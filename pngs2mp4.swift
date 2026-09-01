// Encode a PNG sequence to H.264 MP4 with AVFoundation.
//
// Written rather than reached for because ffmpeg is not installed here and this
// needs nothing beyond the Command Line Tools that are already present.
//
//   swiftc -O pngs2mp4.swift -o pngs2mp4
//   ./pngs2mp4 <outfile.mp4> <fps> <mbps> <frame1.png> <frame2.png> ...

import AVFoundation
import AppKit

let args = CommandLine.arguments
guard args.count > 4 else {
    FileHandle.standardError.write("usage: pngs2mp4 out.mp4 fps mbps frames...\n".data(using: .utf8)!)
    exit(2)
}
let outURL = URL(fileURLWithPath: args[1])
let fps    = Int32(args[2]) ?? 30
let mbps   = Double(args[3]) ?? 12
let frames = Array(args[4...])

// dimensions come from the first frame, so the encoder never disagrees with
// what was rendered
guard let first = NSImage(contentsOfFile: frames[0]),
      let firstCG = first.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
    FileHandle.standardError.write("cannot read \(frames[0])\n".data(using: .utf8)!); exit(1)
}
let W = firstCG.width, H = firstCG.height
guard W % 2 == 0, H % 2 == 0 else {
    FileHandle.standardError.write("H.264 needs even dimensions, got \(W)x\(H)\n".data(using: .utf8)!); exit(1)
}

try? FileManager.default.removeItem(at: outURL)
let writer = try AVAssetWriter(outputURL: outURL, fileType: .mp4)

let input = AVAssetWriterInput(mediaType: .video, outputSettings: [
    AVVideoCodecKey: AVVideoCodecType.h264,
    AVVideoWidthKey: W,
    AVVideoHeightKey: H,
    AVVideoCompressionPropertiesKey: [
        AVVideoAverageBitRateKey: Int(mbps * 1_000_000),
        AVVideoMaxKeyFrameIntervalKey: Int(fps),          // a keyframe a second
        AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel,
        AVVideoAllowFrameReorderingKey: true
    ]
])
input.expectsMediaDataInRealTime = false

let adaptor = AVAssetWriterInputPixelBufferAdaptor(
    assetWriterInput: input,
    sourcePixelBufferAttributes: [
        kCVPixelBufferPixelFormatTypeKey as String: Int(kCVPixelFormatType_32BGRA),
        kCVPixelBufferWidthKey as String: W,
        kCVPixelBufferHeightKey as String: H
    ])

writer.add(input)
writer.startWriting()
writer.startSession(atSourceTime: .zero)

let cs = CGColorSpaceCreateDeviceRGB()
var written = 0

for (i, path) in frames.enumerated() {
    guard let img = NSImage(contentsOfFile: path),
          let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        FileHandle.standardError.write("skip unreadable \(path)\n".data(using: .utf8)!); continue
    }
    var pb: CVPixelBuffer?
    CVPixelBufferPoolCreatePixelBuffer(nil, adaptor.pixelBufferPool!, &pb)
    guard let buf = pb else { continue }

    CVPixelBufferLockBaseAddress(buf, [])
    if let ctx = CGContext(data: CVPixelBufferGetBaseAddress(buf),
                           width: W, height: H, bitsPerComponent: 8,
                           bytesPerRow: CVPixelBufferGetBytesPerRow(buf),
                           space: cs,
                           bitmapInfo: CGImageAlphaInfo.noneSkipFirst.rawValue
                                     | CGBitmapInfo.byteOrder32Little.rawValue) {
        // flatten onto white — the page has no transparency, and H.264 has no
        // alpha channel to carry it if it did
        ctx.setFillColor(CGColor(red: 1, green: 1, blue: 1, alpha: 1))
        ctx.fill(CGRect(x: 0, y: 0, width: W, height: H))
        ctx.draw(cg, in: CGRect(x: 0, y: 0, width: W, height: H))
    }
    CVPixelBufferUnlockBaseAddress(buf, [])

    while !input.isReadyForMoreMediaData { usleep(2000) }
    adaptor.append(buf, withPresentationTime: CMTime(value: CMTimeValue(i), timescale: fps))
    written += 1
}

input.markAsFinished()
let done = DispatchSemaphore(value: 0)
writer.finishWriting { done.signal() }
done.wait()

if writer.status == .completed {
    let bytes = (try? FileManager.default.attributesOfItem(atPath: outURL.path)[.size] as? Int) ?? 0
    let secs = Double(written) / Double(fps)
    print(String(format: "  %@  %dx%d  %d frames  %.1fs @ %dfps  %.1f MB",
                 outURL.lastPathComponent, W, H, written, secs, fps,
                 Double(bytes ?? 0) / 1_048_576))
} else {
    FileHandle.standardError.write("encode failed: \(String(describing: writer.error))\n".data(using: .utf8)!)
    exit(1)
}

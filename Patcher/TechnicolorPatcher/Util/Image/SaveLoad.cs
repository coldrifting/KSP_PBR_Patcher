using System.Diagnostics;
using System.Runtime.InteropServices;
using BCnEncoder.Decoder;
using BCnEncoder.Shared;
using CommunityToolkit.HighPerformance;
using SkiaSharp;

namespace TechnicolorPatcher.Util.Image;

public static class SaveLoad
{
    private static readonly Dictionary<string, SKBitmap> Cache = new();

    public static void ClearCache()
    {
        Cache.Clear();
    }
    
    extension(SKBitmap bitmap)
    {
        public void SaveDds(FileInfo filePath)
        {
            bitmap.SavePng(filePath);

            if (Patcher.TexConvPath != null)
            {
                // Convert to DDS
                ProcessStartInfo startInfo = new()
                {
                    CreateNoWindow = true,
                    UseShellExecute = false,
                    FileName = Patcher.TexConvPath.FullName,
                    WindowStyle = ProcessWindowStyle.Hidden,
                    Arguments = $"-y -f BC7_UNORM -o \"{filePath.Directory!.FullName}\" \"{filePath.FullName}\"",
                    RedirectStandardOutput = true
                };

                using Process? process = Process.Start(startInfo);
                if (process != null)
                {
                    process.WaitForExit();
                    if (process.ExitCode != 0)
                    {
                        string texconvOutput = ""; 
                        while (!process.StandardOutput.EndOfStream)
                        {
                            texconvOutput += process.StandardOutput.ReadLine();
                            texconvOutput += "\n";
                        }
                        throw new InvalidOperationException($"Texconv process failed with exit code {process.ExitCode}:\n{texconvOutput}");
                    }
            
                    // Delete PNG
                    filePath.Delete();
                }
                else
                {
                    throw new InvalidOperationException($"Texconv process failed to start");
                }
            }
        }

        public void SavePng(FileInfo filePath)
        {
            byte[]? bytes = bitmap.Encode(SKEncodedImageFormat.Png, 100).ToArray();
            File.WriteAllBytes(filePath.FullName, bytes);
        }
    }

    public static SKBitmap LoadDds(string filePath)
    {
        if (Cache.TryGetValue(filePath, out SKBitmap? image))
        {
            return image.Copy();
        }
        
        using FileStream fs = File.OpenRead(filePath);
        BcDecoder decoder = new BcDecoder();

        // 1. Decode the DDS file into a 2D array of RGBA32 pixels
        Memory2D<ColorRgba32> decodedPixels = decoder.Decode2D(fs);

        int width = decodedPixels.Width;
        int height = decodedPixels.Height;

        // 2. Create an SKBitmap matching the RGBA8888 byte layout of ColorRgba32
        SKImageInfo imageInfo = new(width, height, SKColorType.Rgba8888, SKAlphaType.Unpremul);
        SKBitmap bitmap = new(imageInfo);

        // 3. Copy the decoded pixel data into the SKBitmap's unmanaged memory buffer
        Span<byte> destinationBytes = bitmap.GetPixelSpan();
        int rowByteSize = width * 4; // 4 bytes per pixel (R, G, B, A)

        for (int y = 0; y < height; y++)
        {
            ReadOnlySpan<ColorRgba32> sourceRow = decodedPixels.Span.GetRowSpan(y);
            ReadOnlySpan<byte> sourceRowBytes = MemoryMarshal.AsBytes(sourceRow);

            Span<byte> destinationRowBytes = destinationBytes.Slice(y * bitmap.RowBytes, rowByteSize);
            sourceRowBytes.CopyTo(destinationRowBytes);
        }

        Cache[filePath] = bitmap.Copy();
        
        return bitmap;
    }
}
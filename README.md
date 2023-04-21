# animate


<img src="https://github.com/r-zachary-murray/animate/blob/main/animation.gif" width="400" height="400" />

## Documentation:

This animate module was developed to make producing high-quality animations with Matplotlib easier. It works by exporting a series of images as png files before combining them with ffmpeg.  This is an intensive operation, but worth it for the quality of the results.  

The module has two main functions, a **savefigures** command which automatically saves a grid of figures as png files, and a **render** command which uses the subprocess module to act as a thin wrapper over ffmpeg. The render function has several features, that bear noting.  First, it automatically sets reasonable defaults for conversion into several formats, including 'mp4' files (most useful in google slides or PowerPoint or slack), 'gif' files (useful for web development and other formats.  It automatically handles codex choice and palette generation for video and gif formats respectively.  The choices available for output_formats are:

1. 'gif'
2. 'avi'
3. 'mp4'
4. 'whatsapp'
5. 'gifbyavi'

Where here, 'whatsapp' uses a format that works well with Facebook applications (WhatsApp, Messenger etc. )
and 'gifbyavi' uses an 'avi' video file as an intermediary between the input frames and output gif. This approach can improve the quality of the gif in some cases.

Finally, there are the cleanup options, which control how our temporary frames are treated.  Three are implemented. '7z', 'None', and 'rm'.  None simply leaves the frames alone after they are generated - this is useful if one wants to export animations in several different formats.  'rm' removes the frames. finally '7z' compresses the frames using 7zip. 


This script uses the subprocess module and has only been tested on Linux-based systems. This may not work correctly on Windows. Finally, it depends on ffmpeg and 7zip being installed. These can be installed with the following commands:

```
sudo apt install ffmpeg
sudo apt-get install p7zip-full
```

See example.ipynb for the syntax

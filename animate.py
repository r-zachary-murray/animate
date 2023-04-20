import subprocess
import os, os.path
import matplotlib
import matplotlib.pyplot as plt
import gc
from tqdm import tqdm
matplotlib.use('agg')

def savefigures(generator,parameter_grid,outdir='./untitled/',dpival=300,trans=False):
    """
    savefigures automates figure saving. Inputs are:
    generator : function of a single input that returns 'fig' objects
    parameter_grid: grid of inputs
    outdir: (optional) output directory
    dpival: (optional) output dpi
    """
    if not os.path.exists(outdir):
        print("saving figures")
        os.makedirs(outdir)
        for i in tqdm(range(len(parameter_grid))):
            fig = generator(parameter_grid[i]) #entris are figures
            fig.savefig(outdir+str(i)+'.png',dpi=dpival,bbox_inches='tight',pad_inches=0.0,transparent=trans)
            fig.clf()
            plt.close(fig)
        return None
    else:
        print('error directory exists, try removing previous attempts!')
        return None


#we want this to utput in a few different formats, avi,mp4, gif and whatsapp. 
#we want to specify either the framerate or the runtime

def render(loc,name,output_type,framerate=None,runtime=None,cleanup_type='7z'):
    """
    render automates figure rendering with ffmpeg. Inputs are:
    loc: location of the input
    name : name of the output animation
    output_type: format of the output options are avi,mp4,whatsapp,gif
    framerate: (optional) output framerate (either framerate or runtime must be specified)
    runtime: (optional) output runtime (either framerate or runtime must be specified)
    cleanup: (optional) specifies cleanup method, options are 7z or None, default is 7z. 
    """

    length = len([name for name in os.listdir(loc) if os.path.isfile(loc+name)])

    if runtime == None and framerate == None and output_type != 'gif':
        print("please specify either a runtime or a framerate")
        return None
    elif runtime == None:
        rate = framerate
    elif framerate == None:
        rate = max([1,int(length/runtime)]) #don't allow less than 1fps by division.

    if output_type != 'gif':
        if rate < 15: #print warning if framerate is low and we're not doing gifs
            print("warning... less than 15 fps!")

    print("Framerate is",rate,'fps')
    print("Total Runtime is",runtime,'s')


    if output_type == 'avi':
        script = 'ffmpeg -framerate '+str(rate)+' -i %d.png -qscale:v 0 ../'+name+'.avi'
        #we'll use call since it blocks and ffmpeg is a parallelized script
        subprocess.call(script, shell=True, cwd=loc)

    if output_type == 'mp4':
        script = 'ffmpeg -framerate '+str(rate)+' -i %d.png -c:v libx264 -qp 0 -f mp4 ../'+name+'.mp4'
        #we'll use call since it blocks and ffmpeg is a parallelized script
        subprocess.call(script, shell=True, cwd=loc)

    if output_type == 'whatsapp':
        script = 'ffmpeg -framerate '+str(rate)+' -i %d.png -vf scale=1280:-2 -c:v libx264 -profile:v baseline -level 3.0 -pix_fmt yuv420p ../'+name+'.mp4'
        #we'll use call since it blocks and ffmpeg is a parallelized script
        subprocess.call(script, shell=True, cwd=loc)

    if output_type == 'gif':
        script1 = 'ffmpeg -i %d.png -vf palettegen ../temp_palette_'+name+'.png'
        script2 = 'ffmpeg -i %d.png -i ../temp_palette_'+name+'.png -lavfi paletteuse ../'+name+'.gif'
        #we'll use call since it blocks and ffmpeg is a parallelized script
        subprocess.call(script1, shell=True, cwd=loc)
        subprocess.call(script2, shell=True, cwd=loc)


    if output_type == 'gifbyavi':
        script1 = 'ffmpeg -framerate '+str(rate)+' -i %d.png -qscale:v 0 ../'+name+'.avi'
        script2 = 'ffmpeg -i ../'+name+'.avi -vf palettegen ../temp_palette_'+name+'.png'
        script3 = 'ffmpeg -i ../'+name+'.avi -i ../temp_palette_'+name+'.png -lavfi paletteuse ../'+name+'.gif'
        #we'll use call since it blocks and ffmpeg is a parallelized script
        subprocess.call(script1, shell=True, cwd=loc)
        subprocess.call(script2, shell=True, cwd=loc)
        subprocess.call(script3, shell=True, cwd=loc)

    ## cleanup stage
    if output_type == 'gif':
        subprocess.call('rm ../temp_palette_'+name+'.png', shell=True, cwd=loc)

    if output_type == 'gifbyavi':
        subprocess.call('rm ../'+name+'.avi', shell=True, cwd=loc)
        subprocess.call('rm ../temp_palette_'+name+'.png', shell=True, cwd=loc)


    if cleanup_type == '7z':
        script1 = '7z a -r ../'+loc.split('/')[1]+'.7z'
        parent = ('/').join(loc.split('/')[:-2])+'/'
        script2 = 'rm -r '+loc[:-1]

        subprocess.call(script1, shell=True, cwd=loc)
        subprocess.call(script2, shell=True, cwd=parent)

    if cleanup_type == 'None' or cleanup_type == None:
        dumvar=1 #do nothing

    if cleanup_type == 'rm':
        parent = ('/').join(loc.split('/')[:-2])+'/'
        script2 = 'rm -r '+loc[:-1]
        subprocess.call(script2, shell=True, cwd=parent) 

    else:
        print("no cleanup type specified")


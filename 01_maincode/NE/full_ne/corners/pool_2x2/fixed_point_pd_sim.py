import numpy as np
import os
from scipy.ndimage.filters import correlate as convolveim
import copy

def bindigits(n, bits):
    s = bin(int(n) & int("1"*bits, 2))[2:]
    return ("{0:0>%s}" % (bits)).format(s)

def hexify(binstring):
    hstr = '%0*x' % ((len(binstring) + 3) // 4, int(binstring, 2))
    return hstr


def convolution_relu(x, w, b):
    x = x.astype(np.int32)
    w = w.astype(np.int32)
    b = b.astype(np.int32)
    H, W, C = x.shape
    HH, WW, C, F = w.shape

    xpad = np.pad(x, ((2,2),(2,2),(0,0)), 'constant', constant_values=((0,0),(0,0),(0,0)))

    out = np.zeros((H,W,F), dtype=np.int8)
    out_relu = np.zeros((H,W,F), dtype=np.int8)
    
    for f in range(F):
        for hp in range(H):
            for wp in range(W):
                out[hp,wp,f] = ((np.sum(xpad[hp:hp+HH,wp:wp+WW,:] * w[:,:,:,f]) + b[f]) >> 8).astype(np.int8)
                out_relu[hp,wp,f] = max(out[hp,wp,f],0)

    return out, out_relu


def max_pool(x, kernel_size=2, stride=2):
    x = x.astype(np.int8)
    H, W, C = x.shape

    xpad = np.pad(x, ((0,0),(0,0),(0,0)), 'constant', constant_values=((0,0),(0,0),(0,0)))

    out = np.zeros((int(H/2),int(W/2),C))

    for c in range(C):
        for hp in range(0, H, stride):
            for wp in range(0, W, stride):
                if (hp+stride <= H) and (wp+stride <= W): # <= to prevent skipping bottom
                    out[int(hp/stride),int(wp/stride),c] = np.max(xpad[hp:hp+kernel_size,wp:wp+kernel_size,c])

    return out


if __name__ == '__main__':
    data_dir = os.getcwd() + '/weight_files/'
    conv1w = np.load(data_dir + 'conv1w.npy').astype(np.int8).transpose(2,3,1,0)
    conv1b = np.load(data_dir + 'conv1b.npy').astype(np.int8)

    img = np.zeros((32,32,8), dtype=np.int8)

    f = open(data_dir + '../macroblocks.mem')

    count = 0
    for binstring in f:
        binstring = binstring.strip()
        #pixelvals = np.array([int(binstring[i:i+8],2) for i in range(0,len(binstring),8)]).astype(np.uint8)
        pixelvals = np.array([int(binstring[i:i+2],16) for i in range(0,len(binstring),2)]).astype(np.uint8)
        # count 0-15, upper left corner r=0-15,c=0-15
        if count < 16:
            img[count,0:16,0] = pixelvals
         # count 16-31, upper right corner r=0-15,c=16-31
        elif count < 32:
            img[count-16,16:32,0] = pixelvals
         # count 32-47, bottom left corner r=16-31,c=0-15
        elif count < 48:
            img[count-16,0:16,0] = pixelvals
         # count 48-63, bottom right corner r=16-31,c=16-31
        else:
            img[count-32,16:32,0] = pixelvals
        count += 1

    print('Weights and input loaded successfully')
    print('Shape Sanity Check #####################')
    print('input shape: {}'.format(img.shape))
    print('conv1 shape: {}'.format(conv1w.shape))
    print('conv1 bias shape: {}'.format(conv1b.shape))

    print('###### Dumping input_msb_lsb.txt')

    f = open(data_dir + 'input_msb_lsb.txt', 'w')

    mbs = [img[0:8,0:8,:], img[0:8,8:16,:], img[0:8,16:24,:], img[0:8,24:32,:],
            img[8:16,0:8,:], img[8:16,8:16,:], img[8:16,16:24,:], img[6:16,24:32,:],
            img[16:24,0:8,:], img[16:24,8:16,:], img[16:24,16:24,:], img[16:24,24:32,:],
            img[24:32,0:8,:], img[24:32,8:16,:], img[24:32,16:24,:], img[24:32,24:32,:]]

    line_count = 0
    linestr = ''
    for m in range(len(mbs)):
        for i in range(mbs[m].shape[0]):
            for j in range(mbs[m].shape[1]):
                # Check to see if need to start new line
                if line_count > 7:
                    f.write(hexify(linestr) + '\n')
                    linestr = ''
                    line_count = 0

                pixs = mbs[m][i,j,:]
                for k in range(len(pixs)):
                    linestr =  bindigits(pixs[k], 8) + linestr
                line_count += 1

    f.close()

    print('####### Dumping input.npy')
    with open(data_dir + 'input.npy', 'wb') as f:
        np.save(f, img)

    outconv1, outconv1relu = convolution_relu(img, conv1w, conv1b)
    print('Conv1+relu output shape: {}, {}'.format(outconv1.shape, outconv1relu.shape))

    print('###### Dumping outconv1_msb_lsb.txt and outconv1relu_msb_lsb.txt')


    f1 = open(data_dir + 'outconv1_msb_lsb.txt', 'w')
    f2 = open(data_dir + 'outconv1relu_msb_lsb.txt', 'w')


    # 32 x 32 x 16

    mbs1 = [outconv1[0:8,0:8,0:8]     , outconv1[0:8,0:8,8:16]    ,
            outconv1[0:8,8:16,0:8]    , outconv1[0:8,8:16,8:16]   ,
            outconv1[0:8,16:24,0:8]   , outconv1[0:8,16:24,8:16]  ,
            outconv1[8:16,0:8,0:8]    , outconv1[8:16,0:8,8:16]   ,
            outconv1[8:16,8:16,0:8]   , outconv1[8:16,8:16,8:16]  ,
            outconv1[8:16,16:24,0:8]  , outconv1[8:16,16:24,8:16] ,
            outconv1[16:24,0:8,0:8]   , outconv1[16:24,0:8,8:16]  ,
            outconv1[16:24,8:16,0:8]  , outconv1[16:24,8:16,8:16] ,
            outconv1[16:24,16:24,0:8] , outconv1[16:24,16:24,8:16],
            outconv1[24:32,0:8,0:8]   , outconv1[24:32,0:8,8:16]  , 
            outconv1[24:32,8:16,0:8]  , outconv1[24:32,8:16,8:16] ,
            outconv1[24:32,16:24,0:8] , outconv1[24:32,16:24,8:16]]

    mbs2 = [outconv1relu[0:8,0:8,0:8]     , outconv1relu[0:8,0:8,8:16]    ,
            outconv1relu[0:8,8:16,0:8]    , outconv1relu[0:8,8:16,8:16]   ,
            outconv1relu[0:8,16:24,0:8]   , outconv1relu[0:8,16:24,8:16]  ,
            outconv1relu[8:16,0:8,0:8]    , outconv1relu[8:16,0:8,8:16]   ,
            outconv1relu[8:16,8:16,0:8]   , outconv1relu[8:16,8:16,8:16]  ,
            outconv1relu[8:16,16:24,0:8]  , outconv1relu[8:16,16:24,8:16] ,
            outconv1relu[16:24,0:8,0:8]   , outconv1relu[16:24,0:8,8:16]  ,
            outconv1relu[16:24,8:16,0:8]  , outconv1relu[16:24,8:16,8:16] ,
            outconv1relu[16:24,16:24,0:8] , outconv1relu[16:24,16:24,8:16],
            outconv1relu[24:32,0:8,0:8]   , outconv1relu[24:32,0:8,8:16]  , 
            outconv1relu[24:32,8:16,0:8]  , outconv1relu[24:32,8:16,8:16] ,
            outconv1relu[24:32,16:24,0:8] , outconv1relu[24:32,16:24,8:16]]


    for m in range(len(mbs1)):
        for i in range(mbs1[m].shape[0]):
            line_count = 0
            linestr = ''
            for j in range(mbs1[m].shape[1]):
                pixs = mbs1[m][i,j,:]
                for k in range(len(pixs)):
                    pixxx = np.uint8(np.int8(pixs[k]))
                    linestr = str(format(pixxx, 'x')).zfill(2) + linestr
                line_count += 1
                if line_count > 7:
                    hexxx = linestr
                    f1.write(str(hexxx)+ '\n')
                    linestr = ''
                    line_count = 0

    for m in range(len(mbs2)):
        for i in range(mbs2[m].shape[0]):
            line_count = 0
            linestr = ''
            for j in range(mbs2[m].shape[1]):
                pixs = mbs2[m][i,j,:]
                for k in range(len(pixs)):
                    pixxx = np.uint8(np.int8(pixs[k]))
                    linestr = str(format(pixxx, 'x')).zfill(2) + linestr
                line_count += 1
                if line_count > 7:
                    hexxx = linestr
                    f2.write(str(hexxx)+ '\n')
                    linestr = ''
                    line_count = 0

    f1.close()
    f2.close()

    print('###### Dumping conv1out.npy and conv1outrelu.npy')
    with open(data_dir + 'conv1out.npy', 'wb') as f:
        np.save(f, outconv1)
    with open(data_dir + 'conv1outrelu.npy', 'wb') as f:
        np.save(f, outconv1relu)
    
    outmaxpool1 = max_pool(outconv1relu)
    print('Max Pool 1 output shape: {}'.format(outmaxpool1.shape))

    print('###### Dumping outmaxpool1_msb_lsb.txt')
    f = open(data_dir + 'outmaxpool1_msb_lsb.txt', 'w')

    # ....and the format gets even weirder for the results of pools
    mbs  = [outmaxpool1[0:4,0:8,0:8]     , outmaxpool1[0:4,0:8,8:16]   ,
            outmaxpool1[0:4,8:16,0:8]    , outmaxpool1[0:4,8:16,8:16]  ,
            outmaxpool1[4:8,0:8,0:8]     , outmaxpool1[4:8,0:8,8:16]   ,
            outmaxpool1[4:8,8:16,0:8]    , outmaxpool1[4:8,8:16,8:16]  ,
            outmaxpool1[8:12,0:8,0:8]    , outmaxpool1[8:12,0:8,8:16]  ,
            outmaxpool1[8:12,8:16,0:8]   , outmaxpool1[8:12,8:16,8:16] ,
            outmaxpool1[12:16,0:8,0:8]   , outmaxpool1[12:16,0:8,8:16] ,
            outmaxpool1[12:16,8:16,0:8]  , outmaxpool1[12:16,8:16,8:16]]

    # reset counts here since outmaxpool chunks are < 8 rows
    line_count = 0
    linestr = ''
    for m in range(len(mbs)):
        for i in range(mbs[m].shape[0]):
            for j in range(mbs[m].shape[1]):
                pixs = copy.deepcopy(mbs[m][i,j,:])
                for k in range(len(pixs)):
                    pixxx = np.uint8(np.int8(pixs[k]))
                    linestr = str(format(pixxx, 'x')).zfill(2) + linestr
                line_count += 1
                if line_count > 7:
                    hexxx = linestr
                    f.write(str(hexxx)+ '\n')
                    linestr = ''
                    line_count = 0

    f.close()

    print('###### Dumping maxpool1out.npy')
    with open(data_dir + 'maxpool1out.npy', 'wb') as f:
        np.save(f, outmaxpool1)


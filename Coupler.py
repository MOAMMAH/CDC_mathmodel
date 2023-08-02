
######## IMPORTS ########
# General purpose imports
import lumapi
import numpy as np
from scipy.constants import c



def Switch2Layout(mode):
    mode.switchtolayout()
    mode.selectall()
    mode.delete()

def IOWG(mode,w1,w2,gap,waveguidehight):       
    # up input output waveguides
    mode.addrect();
    mode.set("name", "input_WG");
    mode.set("material", Silicon);
    mode.set("x min", cdcstart-wg_length);
    mode.set("x max", cdcstart);
    mode.set("y",  w1);
    mode.set("y span", w1);
    mode.set("z min", 0);
    mode.set("z max", waveguidehight);

    
    mode.select("input_WG");
    input_ymin = mode.get("y min");

    mode.addrect();
    mode.set("name", "drop_WG");
    mode.set("material", Silicon);
    mode.set("x min", cdcstart-wg_length);
    mode.set("x max", cdcstart);
    mode.set("y max",input_ymin-gap);
    mode.set("y min", input_ymin-w2-gap);
    mode.set("z min", 0);
    mode.set("z max", waveguidehight);


def EigenMode(mode,w1,w2):
    mode.select("input_WG");
    input_y = mode.get("y");
    input_max_Y = mode.get("y max");
    mode.select("drop_WG");
    drop_y = mode.get("y");
    drop_min_Y = mode.get("y min");
    FDE_Y= (input_y+drop_y)/2;

    mode.addfde();
    mode.set("background material", SIO2);
    mode.set("solver type", "2D X normal");
    mode.set("x",cdcstart-space/2);

    mode.set("y", FDE_Y);
    mode.set("y span", w1+w2+deltaw1+deltaw2+space);

    mode.set("z min", -1.5e-6);
    mode.set("z max", 1e-6);

    mode.set("y min bc", "PML");
    mode.set("y max bc", "PML");
    mode.set("z min bc", "PML");
    mode.set("z max bc", "PML");
    mode.set("define y mesh by", "maximum mesh step");
    mode.set("dy", 10e-9);
    mode.set("define z mesh by", "maximum mesh step");
    mode.set("dz", 10e-9);



def neff1(mode, wavelength):
    #setanalysis
    mode.setanalysis("number of trial modes", 2);
    mode.setanalysis("wavelength", wavelength);
    mode.findmodes();
    mode.selectmode(1);
    neff = mode.getdata("mode1","neff");
    neff=np.real(neff)
    return neff;

def neff2(mode, wavelength):
    #setanalysis
    mode.setanalysis("number of trial modes", 2);
    mode.setanalysis("wavelength", wavelength);
    mode.findmodes();
    mode.selectmode(2);
    neff = mode.getdata("mode2","neff");
    neff=np.real(neff)
    return neff;

def DataBase(mode,lamd,w1,w2):
    wvl=np.linspace(lamd[0],lamd[-1],5)
    w1 = np.linspace(w1[0],w1[-1],5)
    w2 = np.linspace(w2[0],w2[-1],5)
    neff1Data= np.zeros((5,5,5))
    neff2Data= np.zeros((5,5,5))
    for i in range(5):
        for j in range(5):
            for k in range(5):
                IOWG(mode,w1[i],w2[j],gap,waveguidehight)
                EigenMode(mode,w1[i],w2[j])
                neff1Data[i,j,k]=neff1(mode,wvl[k])
                Switch2Layout(mode)
    save3darray(neff1Data, 'neff1_DATABASE.txt')

    for i in range(5):
        for j in range(5):
            for k in range(5):
                IOWG(mode,w1[j],w2[i],gap,waveguidehight)
                EigenMode(mode,w1[j],w2[i])
                neff2Data[i,j,k]=neff2(mode,wvl[k])
                Switch2Layout(mode)
    save3darray(neff2Data, 'neff2_DATABASE.txt')              



#define a function to save the 3d array in a txt file
def save3darray(array, filename):
    with open(filename, 'w') as outfile:
        #outfile.write('# Array shape: {0}\n'.format(array.shape))
        for data_slice in array:
            np.savetxt(outfile, data_slice, fmt='%-7.7f')
            outfile.write('\n')    

#function for w1_w2_lambda.txt file
def w1_w2_lambda(w1,w2,lamda): 
    w1=np.linspace(w1[0],w1[-1],5)
    w2=np.linspace(w2[0],w2[-1],5)
    lamda=np.linspace(lamda[0],lamda[-1],5)
    #save w1 ,w2, lamda in three lines of a txt file without brackets
    with open('w1_w2_lambda.txt', 'w') as outfile:
        outfile.write('{0}\n'.format(w1))
        outfile.write('{0}\n'.format(w2))
        outfile.write('{0}\n'.format(lamda))
    
    with open('w1_w2_lambda.txt', 'r') as file:
        lines = file.readlines()
        l_line = []
        # Iterate through each line and remove the brackets and save the file
        for line in lines:
            l_line.append(line)
    file.close()
    with open('w1_w2_lambda.txt', 'w') as outfile:
        for line in l_line:
            values = line.replace('[', '')
            values = values.replace(']', '')
            outfile.write(values)

     

 
if __name__ == "__main__":
    Silicon = "Si (Silicon) - Palik"
    SIO2="SiO2 (Glass) - Palik"
    ## CLEAR SESSION
    gap =200e-9;#200e-9
    # w1 = 440e-9; #waveguide width  #430 , 550
    # w2 = 560e-9;
    w1=[550e-9, 570e-9]
    w2=[430e-9, 450e-9]
    Landa=[1.4e-6, 1.7e-6] #wavelength
    waveguidehight = 220e-9;
    N=800; #519 (N+1)*2 =Ntotal
    N=(N/2)-1;
    cdcstart=-6e-6;
    dw=25e-9; #delta w 
    deltaw2 = 38e-9; #28e-9
    deltaw1=32e-9;  #48e-9
    Landa_1= 318e-9; #lambda/2 312e-9
    Landa_2=321e-9;
    wg_length = 2e-6; #input waveguide length
    space=1e-6;
    mode = lumapi.MODE(hide = False)
    Switch2Layout(mode)
    #IOWG(mode,w1,w2,gap,waveguidehight)
    #EigenMode(mode)
    try:
        DataBase(mode,Landa,w1,w2)
        w1_w2_lambda(w1,w2,Landa)
        print('<------> Data base is saved! <------>')
    except:
        print('Error occured!')

    

    #input('Press Enter to escape...')







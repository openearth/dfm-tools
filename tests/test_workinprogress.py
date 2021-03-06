# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 01:19:24 2020

@author: veenstra
"""

import pytest
import inspect
import os

from dfm_tools.testutils import getmakeoutputdir, gettestinputdir
dir_testinput = gettestinputdir()



@pytest.mark.acceptance
def test_trygetondepth():
    import numpy as np
    from netCDF4 import Dataset
    
    from dfm_tools.get_nc import get_ncmodeldata#, get_netdata
    from dfm_tools.get_nc_helpers import get_varname_fromnc
    
    #code from test_get_nc test d
    file_nc = os.path.join(dir_testinput,r'DFM_sigma_curved_bend\DFM_OUTPUT_cb_3d\cb_3d_map.nc')
    
    timestep = 72
    #layno = 5
    #calcdist_fromlatlon = None
    multipart = None
    #line_array = np.array([[ 104.15421399, 2042.7077107 ],
    #                       [2913.47878063, 2102.48057382]])
    #val_ylim = None
    #clim_bl = None
    #optimize_dist = None
    #ugrid = get_netdata(file_nc=file_nc, multipart=multipart)
    #intersect_gridnos, intersect_coords = ugrid.polygon_intersect(line_array, optimize_dist=None)
    
    
    #code from get_xzcoords_onintersection
    data_nc = Dataset(file_nc)
    
    varn_mesh2d_s1 = get_varname_fromnc(data_nc,'mesh2d_s1', vardim='var')
    data_frommap_wl3 = get_ncmodeldata(file_nc, varname=varn_mesh2d_s1, timestep=timestep, multipart=multipart)
    data_frommap_wl3 = data_frommap_wl3[0,:]
    #data_frommap_wl3_sel = data_frommap_wl3[0,intersect_gridnos]
    varn_mesh2d_flowelem_bl = get_varname_fromnc(data_nc,'mesh2d_flowelem_bl', vardim='var')
    data_frommap_bl = get_ncmodeldata(file_nc, varname=varn_mesh2d_flowelem_bl, multipart=multipart)
    #data_frommap_bl_sel = data_frommap_bl[intersect_gridnos]
    
    dimn_layer = get_varname_fromnc(data_nc,'nmesh2d_layer', vardim='dim')
    if dimn_layer is None: #no layers, 2D model
        nlay = 1
    else:
        nlay = data_nc.dimensions[dimn_layer].size
    
    varn_layer_z = get_varname_fromnc(data_nc,'mesh2d_layer_z', vardim='var')
    if varn_layer_z is None:
        laytyp = 'sigmalayer'
        #zvals_cen = np.linspace(data_frommap_bl_sel,data_frommap_wl3_sel,nlay)
        #zvals_interface = np.linspace(data_frommap_bl_sel,data_frommap_wl3_sel,nlay+1)
        zvals_interface = np.linspace(data_frommap_bl,data_frommap_wl3,nlay+1)
    else:
        laytyp = 'zlayer'
        #zvals_cen = get_ncmodeldata(file_nc=file_map, varname='mesh2d_layer_z', lay='all')#, multipart=False)
        #zvals_interface = get_ncmodeldata(file_nc=file_map, varname='mesh2d_interface_z')#, multipart=False)
        zvals_interface = data_nc.variables['mesh2d_interface_z'][:]
    
    print(laytyp)
    depth = -1
    z_test_higher = np.argmax((zvals_interface > depth),axis=0)
    z_test_lower = np.argmin((zvals_interface < depth),axis=0)
    z_test_all = z_test_higher==z_test_lower
    




@pytest.mark.acceptance
def test_delft3D_netcdf():
    dir_output = getmakeoutputdir(__file__,inspect.currentframe().f_code.co_name)
    """
    to get delft3D to write netCDF output instead of .dat files, add these lines to your mdf:
        FlNcdf= #maphis#
        ncFormat=4

    NO: it is also possible to convert existing Delft3D4 output with getdata.pl, but Delft3D models that were converted with getdata.pl often give corrupt variables (see comments in code for details) since NEFIS conversion is not fully up to date in getdata.pl.
    YES: it is recommended to rerun your Delft3D model with netCDF output instead with above lines
    get the netcdf files via putty with:
        module load simona
        cd /p/1220688-lake-kivu/3_modelling/1_FLOW/7_heatfluxinhis/063
        getdata.pl -f trim-thiery_002_coarse.dat -v S1,U1,V1,ALFAS,QEVA -o netcdf
        http://simona.deltares.nl/release/doc/usedoc/getdata/getdata.pdf
        #double precision in trimfile causes this conversion to fail, use netCDF output in Delft3D instead
        
    get the netcdf files via putty with:
        module load simona
        cd ./D3D_3D_sigma_curved_bend
        getdata.pl -f trim-cb2-sal-added-3d.dat -v S1,U1,V1,ALFAS -o netcdf
        getdata.pl -f trih-cb2-sal-added-3d.dat -v ZWL,ZCURU,ZCURV,ALFAS,NAMST -o netcdf
        http://simona.deltares.nl/release/doc/usedoc/getdata/getdata.pdf
        #faulty data in NAMST variable, station names are not available


    dir_output = './test_output'
    """
    
    import numpy as np
    import datetime as dt
    import matplotlib.pyplot as plt
    plt.close('all')
    
    from dfm_tools.get_nc import get_ncmodeldata#, get_netdata, plot_netmapdata
    from dfm_tools.get_nc_helpers import get_ncvardimlist, get_hisstationlist#, get_varname_fromnc
    from dfm_tools.regulargrid import uva2xymagdeg
    from dfm_tools.io.polygon import Polygon

    file_ldb = r'p:\1220688-lake-kivu\3_modelling\1_FLOW\4_CH4_CO2_included\008\lake_kivu_geo.ldb'
    data_ldb = Polygon.fromfile(file_ldb, pd_output=True)

    file_nc = r'p:\1220688-lake-kivu\3_modelling\1_FLOW\7_heatfluxinhis\062_netcdf\trim-thiery_002_coarse.nc'
    vars_pd, dims_pd = get_ncvardimlist(file_nc=file_nc)
    
    data_nc_XZ = get_ncmodeldata(file_nc=file_nc, varname='XZ')
    data_nc_YZ = get_ncmodeldata(file_nc=file_nc, varname='YZ')
    data_nc_XCOR = get_ncmodeldata(file_nc=file_nc, varname='XCOR')
    data_nc_YCOR = get_ncmodeldata(file_nc=file_nc, varname='YCOR')
    data_nc_ALFAS = get_ncmodeldata(file_nc=file_nc, varname='ALFAS') #contains rotation of all cells wrt real world
    #data_nc_S1 = get_ncmodeldata(file_nc=file_nc, varname='S1',timestep='all')
    data_nc_QNET = get_ncmodeldata(file_nc=file_nc, varname='QNET',timestep='all')
    data_nc_DPV0 = get_ncmodeldata(file_nc=file_nc, varname='DPV0')
    #data_nc_QEVA = get_ncmodeldata(file_nc=file_nc, varname='QEVA',timestep='all')
    data_nc_KCU = get_ncmodeldata(file_nc=file_nc, varname='KCU')
    data_nc_KCV = get_ncmodeldata(file_nc=file_nc, varname='KCV')
    
    layno=-2
    data_nc_U1 = get_ncmodeldata(file_nc=file_nc, varname='U1',timestep='all',layer=layno)
    data_nc_V1 = get_ncmodeldata(file_nc=file_nc, varname='V1',timestep='all',layer=layno)
    
    mask_XY = (data_nc_XZ==0) & (data_nc_YZ==0)
    data_nc_XZ[mask_XY] = np.nan
    data_nc_YZ[mask_XY] = np.nan
    mask_XYCOR = (data_nc_XCOR<=-999.999) & (data_nc_YCOR<=-999.999)
    data_nc_XCOR[mask_XYCOR] = np.nan
    data_nc_YCOR[mask_XYCOR] = np.nan
    

    
    fig, ax = plt.subplots()
    ax.plot(data_nc_XCOR,data_nc_YCOR,'-b',linewidth=0.2)
    ax.plot(data_nc_XCOR.T,data_nc_YCOR.T,'-b',linewidth=0.2)
    ax.set_aspect('equal')
    plt.savefig(os.path.join(dir_output,'kivu_mesh'))
    
    fig, axs = plt.subplots(1,3, figsize=(16,7))
    for iT, timestep in enumerate([1,10,15]):
        ax=axs[iT]
        vel_x, vel_y, vel_magn, direction_naut_deg = uva2xymagdeg(U1=data_nc_U1[timestep,0,:,:],V1=data_nc_V1[timestep,0,:,:],ALFAS=data_nc_ALFAS)#,
        #                                                          KCU=data_nc_KCU, KCV=data_nc_KCV)
        #pc = ax.pcolor(data_nc_XCOR,data_nc_YCOR,direction_naut_deg[1:,1:],cmap='jet')
        #pc.set_clim([0,360])
        pc = ax.pcolor(data_nc_XCOR,data_nc_YCOR,vel_magn[1:,1:],cmap='jet')
        pc.set_clim([0,0.15])
        cbar = fig.colorbar(pc, ax=ax)
        cbar.set_label('velocity magnitude (%s)'%(data_nc_U1.var_ncvarobject.units))
        ax.set_title('t=%d (%s)'%(timestep, data_nc_U1.var_times.iloc[timestep]))
        ax.set_aspect('equal')
        ax.quiver(data_nc_XZ[::2,::2], data_nc_YZ[::2,::2], vel_x[::2,::2], vel_y[::2,::2], 
                  scale=3,color='w',width=0.005)#, edgecolor='face', cmap='jet')
    fig.tight_layout()
    plt.savefig(os.path.join(dir_output,'kivu_velocity_pcolor'))

    fig, axs = plt.subplots(1,3, figsize=(16,7))
    for iT, timestep in enumerate([1,10,15]):
        ax=axs[iT]
        vel_x, vel_y, vel_magn, direction_naut_deg = uva2xymagdeg(U1=data_nc_U1[timestep,0,:,:],V1=data_nc_V1[timestep,0,:,:],ALFAS=data_nc_ALFAS)#,
        #                                                          KCU=data_nc_KCU, KCV=data_nc_KCV)
        #pc = ax.pcolor(data_nc_XCOR,data_nc_YCOR,vel_magn[1:,1:],cmap='jet')
        ax.set_title('t=%d (%s)'%(timestep, data_nc_U1.var_times.iloc[timestep]))
        ax.set_aspect('equal')
        pc = ax.quiver(data_nc_XZ[::2,::2], data_nc_YZ[::2,::2], vel_x[::2,::2], vel_y[::2,::2], vel_magn[::2,::2],
                  scale=3,color='w',width=0.005, edgecolor='face', cmap='jet')
        pc.set_clim([0,0.15])
        cbar = fig.colorbar(pc, ax=ax)
        cbar.set_label('velocity magnitude (%s)'%(data_nc_U1.var_ncvarobject.units))
    fig.tight_layout()
    plt.savefig(os.path.join(dir_output,'kivu_velocity'))
    
    #QNET
    fig, axs = plt.subplots(1,3, figsize=(16,7))
    for iT, timestep in enumerate([1,10,15]):
        ax=axs[iT]
        pc = ax.pcolor(data_nc_XZ,data_nc_YZ,data_nc_QNET[iT,:,:],cmap='jet')
        pc.set_clim([-60,60])
        cbar = fig.colorbar(pc, ax=ax)
        cbar.set_label('%s (%s)'%(data_nc_QNET.var_varname, data_nc_QNET.var_ncvarobject.units))
        ax.set_title('t=%d (%s)'%(timestep, data_nc_QNET.var_times.iloc[timestep]))
        ax.set_aspect('equal')
    fig.tight_layout()
    plt.savefig(os.path.join(dir_output,'kivu_Qnet'))

    #BED
    fig, ax = plt.subplots(figsize=(6,8))
    pc = ax.pcolor(data_nc_XZ,data_nc_YZ,data_nc_DPV0,cmap='jet')
    cbar = fig.colorbar(pc, ax=ax)
    cbar.set_label('%s (%s)'%(data_nc_DPV0.var_varname, data_nc_DPV0.var_ncvarobject.units))
    ax.set_aspect('equal')
    fig.tight_layout()
    plt.savefig(os.path.join(dir_output,'kivu_bedlevel'))
    
    
    
    


    #FROM HIS data
    file_nc = r'p:\1220688-lake-kivu\3_modelling\1_FLOW\7_heatfluxinhis\063_netcdf\trih-thiery_002_coarse.nc'
    vars_pd, dims_pd = get_ncvardimlist(file_nc=file_nc)
    
    data_nc_NAMST = get_hisstationlist(file_nc=file_nc, varname='NAMST')
    data_nc_ZWL = get_ncmodeldata(file_nc=file_nc, varname='ZWL',timestep='all',station='all')
    #data_nc_ZCURU = get_ncmodeldata(file_nc=file_nc, varname='ZCURU',timestep='all',station='all',layer='all')
    #data_nc_ZCURV = get_ncmodeldata(file_nc=file_nc, varname='ZCURV',timestep='all',station='all',layer='all')

    fig, ax = plt.subplots(figsize=(16,7))
    for iS in range(10):
        ax.plot(data_nc_ZWL.var_times,data_nc_ZWL[:,iS],label=data_nc_NAMST['NAMST'].iloc[iS], linewidth=1)
    ax.legend()
    ax.set_ylabel('%s (%s)'%(data_nc_ZWL.var_varname, data_nc_ZWL.var_ncvarobject.units))
    ax.set_xlim([data_nc_ZWL.var_times[0],data_nc_ZWL.var_times[0]+dt.timedelta(days=14)])
    plt.savefig(os.path.join(dir_output,'kivu_his_ZWL'))




    #from MAP DATA CURVEDBEND
    file_nc = os.path.join(dir_testinput,'D3D_3D_sigma_curved_bend_nc\\trim-cb2-sal-added-3d.nc')
    vars_pd, dims_pd = get_ncvardimlist(file_nc=file_nc)
    
    data_nc_XZ = get_ncmodeldata(file_nc=file_nc, varname='XZ')
    data_nc_YZ = get_ncmodeldata(file_nc=file_nc, varname='YZ')
    data_nc_XCOR = get_ncmodeldata(file_nc=file_nc, varname='XCOR')
    data_nc_YCOR = get_ncmodeldata(file_nc=file_nc, varname='YCOR')
    data_nc_ALFAS = get_ncmodeldata(file_nc=file_nc, varname='ALFAS') #contains rotation of all cells wrt real world
    data_nc_U1 = get_ncmodeldata(file_nc=file_nc, varname='U1',timestep='all',layer='all')
    data_nc_V1 = get_ncmodeldata(file_nc=file_nc, varname='V1',timestep='all',layer='all')
    #data_nc_S1 = get_ncmodeldata(file_nc=file_nc, varname='S1',timestep='all')
    data_nc_KCU = get_ncmodeldata(file_nc=file_nc, varname='KCU')
    data_nc_KCV = get_ncmodeldata(file_nc=file_nc, varname='KCV')
    
    mask_XY = (data_nc_XZ==0) & (data_nc_YZ==0)
    data_nc_XZ[mask_XY] = np.nan
    data_nc_YZ[mask_XY] = np.nan
    mask_XYCOR = (data_nc_XCOR==0) & (data_nc_YCOR==0)
    data_nc_XCOR[mask_XYCOR] = np.nan
    data_nc_YCOR[mask_XYCOR] = np.nan
    #masking should work but quiver does not read masks for X and Y, so use own
    #data_nc_XZ.mask = mask_XY
    #data_nc_YZ.mask = mask_XY

    fig, ax = plt.subplots()
    ax.plot(data_nc_XCOR,data_nc_YCOR,'-b',linewidth=0.2)
    ax.plot(data_nc_XCOR.T,data_nc_YCOR.T,'-b',linewidth=0.2)
    ax.set_aspect('equal')
    lim_x = [0,4100]
    lim_y = [0,4100]
    ax.set_xlim(lim_x)
    ax.set_ylim(lim_y)
    plt.savefig(os.path.join(dir_output,'curvedbend_mesh'))
    
    txt_abcd = 'abcdefgh'
    var_clim = [0,1.2]
    ncols=2
    fig, axs = plt.subplots(2,ncols, figsize=(8.6,8))
    fig.suptitle('velocity magnitude on four times')
    for iT, timestep in enumerate([0,1,2,4]):
        id0 = int(np.floor(iT/ncols))
        id1 = iT%ncols
        #print('[%s,%s]'%(id0,id1))
        ax=axs[id0,id1]
        vel_x, vel_y, vel_magn, direction_naut_deg = uva2xymagdeg(U1=data_nc_U1[timestep,9,:,:],V1=data_nc_V1[timestep,9,:,:],ALFAS=data_nc_ALFAS)#,
        #                                                          KCU=data_nc_KCU, KCV=data_nc_KCV)
        pc = ax.pcolor(data_nc_XCOR,data_nc_YCOR,vel_magn[1:,1:],cmap='jet')
        pc.set_clim(var_clim)
        #cbar = fig.colorbar(pc, ax=ax)
        #cbar.set_label('velocity magnitude (%s)'%(data_nc_U1.var_ncvarobject.units))
        #ax.set_title('t=%d (%s)'%(timestep, data_nc_U1.var_times.iloc[timestep]))
        ax.set_aspect('equal')
        #ax.quiver(data_nc_XZ[::2,::2], data_nc_YZ[::2,::2], vel_x[::2,::2], vel_y[::2,::2],
        #          scale=15,color='w',width=0.005)#, edgecolor='face', cmap='jet')
        ax.quiver(data_nc_XZ, data_nc_YZ, vel_x, vel_y,
                  scale=25,color='w',width=0.003)#, edgecolor='face', cmap='jet')
        #add grid
        ax.plot(data_nc_XCOR,data_nc_YCOR,'-b',linewidth=0.2)
        ax.plot(data_nc_XCOR.T,data_nc_YCOR.T,'-b',linewidth=0.2)
        #additional figure formatting to tweak the details
        ax.grid(alpha=0.4)
        if id1 != 0:
            ax.get_yaxis().set_ticklabels([])
        else:
            ax.set_ylabel('y dist', labelpad=-0.5)
        if id0 == 0:
            ax.get_xaxis().set_ticklabels([])
        else:
            ax.set_xlabel('x dist')
        ax.tick_params(axis='x', labelsize=9)
        ax.tick_params(axis='y', labelsize=9)
        lim_x = [0,4100]
        lim_y = [0,4100]
        ax.set_xlim(lim_x)
        ax.set_ylim(lim_y)
        ax.text(lim_x[0]+0.02*np.diff(lim_x), lim_y[0]+0.95*np.diff(lim_y), '%s) t=%d (%s)'%(txt_abcd[iT],timestep, data_nc_U1.var_times.iloc[timestep]),fontweight='bold',fontsize=12)
    fig.tight_layout()
    #additional figure formatting to tweak the details
    plt.subplots_adjust(left=0.07, right=0.90, bottom=0.065, top=0.95, wspace=0.03, hspace=0.04)
    cbar_ax = fig.add_axes([0.91, 0.065, 0.02, 0.885])
    cbar = fig.colorbar(pc, cax=cbar_ax, ticks=np.linspace(var_clim[0],var_clim[1],7))
    #cbar_ax.set_xlabel('[%s]'%(data_nc_U1.var_ncvarobject.units))
    cbar_ax.set_ylabel('velocity magnitude [%s]'%(data_nc_U1.var_ncvarobject.units))
    plt.savefig(os.path.join(dir_output,'curvedbend_velocity_pcolor'))



    #FROM HIS data curvedbend
    file_nc = os.path.join(dir_testinput,'D3D_3D_sigma_curved_bend_nc\\trih-cb2-sal-added-3d.nc')
    vars_pd, dims_pd = get_ncvardimlist(file_nc=file_nc)
    
    data_nc_NAMST = get_hisstationlist(file_nc=file_nc, varname='NAMST')
    data_nc_ZWL = get_ncmodeldata(file_nc=file_nc, varname='ZWL',timestep='all',station='all')
    #data_nc_ZCURU = get_ncmodeldata(file_nc=file_nc, varname='ZCURU',timestep='all',station='all',layer='all')
    #data_nc_ZCURV = get_ncmodeldata(file_nc=file_nc, varname='ZCURV',timestep='all',station='all',layer='all')

    fig, ax = plt.subplots(figsize=(16,7))
    for iS in range(5):
        ax.plot(data_nc_ZWL.var_times,data_nc_ZWL[:,iS],label=data_nc_NAMST['NAMST'].iloc[iS], linewidth=1)
    ax.legend()
    ax.set_ylabel('%s (%s)'%(data_nc_ZWL.var_varname, data_nc_ZWL.var_ncvarobject.units))
    ax.set_xlim([data_nc_ZWL.var_times[0],data_nc_ZWL.var_times[0]+dt.timedelta(days=2)])
    plt.savefig(os.path.join(dir_output,'curvedbend_his_ZWL'))






@pytest.mark.acceptance
def test_waqua_netcdf_convertedwith_getdata():
    dir_output = getmakeoutputdir(__file__,inspect.currentframe().f_code.co_name)
    
    """
    RMM testmodel: convert all waqua output to netcdf after completion of the run by adding this to siminp file:
        NETCDFOUTPUT
          MAPS
        	OUTPUTNAME = 'nc_map.nc'
          HISTORIES
        	OUTPUTNAME = 'nc_his.nc'
          OPTIONS
            MAPEXTRA = 'HZETA,VICO'
            HISEXTRA = 'Z0'
        
        waqpro.pl uses netcdfoutput.pm to write map-variables by calling getdata (appended with mapextra):
            getdata.pl -f SDS-haven -o netcdf -d nc_map.nc -v xzeta,yzeta,xdep,ydep,sep,velu,velv,h
        waqpro.pl uses netcdfoutput.pm to write his-variables by calling getdata (appended with hisextra):
            getdata.pl -f SDS-haven -o netcdf -d nc_his.nc -v zwl,namwl,mwl,nwl,xzeta,yzeta,itdate,zcur,zcuru,zcurv,namc,ctr,fltr,namtra,ctrv,fltrv,namtrv
        get a list of all available variables in the SDS file:
            getdata.pl -f SDS-haven -v l
    
    convert entire SDS file with getdata.pl (this gives you a list of variables but does not work yet):
        module load simona
        #mapvars_raw=$(getdata.pl -f SDS-haven -v l | grep 'TIME DEP' | grep MNMAXK | sed 's/\tREAL.*//' | sed 's/\tINT.*//' | tr '\n' ',')
        #hisvars_raw=$(getdata.pl -f SDS-haven -v l | grep 'TIME DEP' | grep -v MNMAXK | sed 's/\tREAL.*//' | sed 's/\tINT.*//' | tr '\n' ',')
        mapvars_raw=$(getdata.pl -f SDS-haven -v l | grep 'TIME DEP' | grep MNMAXK | grep -v "V\S*INT" | sed 's/\tREAL.*//' | sed 's/\tINT.*//' | tr '\n' ',')
        hisvars_raw=$(getdata.pl -f SDS-haven -v l | grep 'TIME DEP' | grep NO | sed 's/\tREAL.*//' | sed 's/\tINT.*//' | tr '\n' ',')
        getdata.pl -f SDS-haven -o netcdf -d nc_map.nc -v ${mapvars_raw%?}
        getdata.pl -f SDS-haven -o netcdf -d nc_his.nc -v ${hisvars_raw%?}

    DCSM: convert existing waqua output to netcdf files via putty with:
        module load simona
        cd /p/1204257-dcsmzuno/2019/DCSMv6/A01
        getdata.pl -f SDS-A01 -v l
        getdata.pl -f SDS-A01 -v SEP,VELU,VELV,YZETA,XZETA -o netcdf -d SDS-A01_map
        getdata.pl -f SDS-A01 -v ZWL,ZCURU,ZCURV,NAMWL,NAMC -o netcdf -d SDS-A01_his
        http://simona.deltares.nl/release/doc/usedoc/getdata/getdata.pdf
        
    OSR: convert existing waqua output to netcdf files via putty with:
        module load simona
        cd /p/archivedprojects/1230049-zoutlastbeperking/Gaten_langsdam/Simulaties/OSR-model_GatenLangsdam/berekeningen/run7
        getdata.pl -f SDS-nsctri -v l
        getdata.pl -f SDS-nsctri -v SEP,VELU,VELV -o netcdf -d SDS-nsctri_map
        getdata.pl -f SDS-nsctri -v ZWL,ZCURU,ZCURV,NAMWL,NAMC -o netcdf -d SDS-nsctri_his
        http://simona.deltares.nl/release/doc/usedoc/getdata/getdata.pdf
        #this file should be recreated with YZETA,XZETA added to map

    RMM: convert existing waqua output to netcdf files via putty with:
        module load simona
        cd /p/11205258-006-kpp2020_rmm-g6/C_Work/07_WAQUAresultaten/j15
        getdata.pl -f SDS-riv_tba -v l
        getdata.pl -f SDS-riv_tba -v SEP,VELU,VELV,YZETA,XZETA -o netcdf -d SDS-riv_tba_map
        getdata.pl -f SDS-riv_tba -v ZWL,ZCURU,ZCURV,NAMWL,NAMC -o netcdf -d SDS-riv_tba_his
        http://simona.deltares.nl/release/doc/usedoc/getdata/getdata.pdf
        
    dir_output = './test_output'
    """
    import datetime as dt
    import numpy as np
    import matplotlib.pyplot as plt
    plt.close('all')
    
    from dfm_tools.get_nc import get_ncmodeldata#, get_netdata, plot_netmapdata
    from dfm_tools.get_nc_helpers import get_ncvardimlist, get_hisstationlist#, get_varname_fromnc
    
    
    #MAP ZUNO
    file_nc = r'p:\1204257-dcsmzuno\2019\DCSMv6\A01\SDS-A01_map.nc'
    vars_pd, dims_pd = get_ncvardimlist(file_nc=file_nc)
    
    data_nc_x = get_ncmodeldata(file_nc=file_nc, varname='grid_x')
    data_nc_y = get_ncmodeldata(file_nc=file_nc, varname='grid_y')
    data_nc_SEP = get_ncmodeldata(file_nc=file_nc, varname='SEP',timestep='all')
    #data_nc_VELU = get_ncmodeldata(file_nc=file_nc, varname='VELU',timestep='all')
    #data_nc_VELV = get_ncmodeldata(file_nc=file_nc, varname='VELV',timestep='all')
    data_nc_xcen = np.mean(data_nc_x, axis=2)
    data_nc_ycen = np.mean(data_nc_y, axis=2)
    
    fig, ax = plt.subplots()
    #vel_x, vel_y, vel_magn, direction_naut_deg = uva2xymagdeg(u=data_nc_U1[timestep,90,:,:],v=data_nc_V1[timestep,90,:,:],alpha=data_nc_ALFAS)
    #pc = ax.pcolor(data_nc_XZ,data_nc_YZ,direction_naut_deg,cmap='jet')
    #pc.set_clim([0,360])
    timestep=0
    pc = ax.pcolor(data_nc_xcen,data_nc_ycen,data_nc_SEP[timestep,:,:],cmap='jet')
    pc.set_clim([-0.1,0.1])
    cbar = fig.colorbar(pc, ax=ax)
    cbar.set_label('%s (%s)'%(data_nc_SEP.var_varname, data_nc_SEP.var_ncvarobject.units))
    ax.set_title('t=%d (%s)'%(timestep, data_nc_SEP.var_times.iloc[timestep]))
    ax.set_aspect('equal')
    #ax.quiver(data_nc_XZ[::2,::2], data_nc_YZ[::2,::2], vel_x[::2,::2], vel_y[::2,::2], 
    #          scale=3,color='w',width=0.005)#, edgecolor='face', cmap='jet')
    fig.tight_layout()
    plt.savefig(os.path.join(dir_output,'waqua_DCSM_map_wl'))

    
    #HIS ZUNO
    file_nc = r'p:\1204257-dcsmzuno\2019\DCSMv6\A01\SDS-A01_his.nc'
    vars_pd, dims_pd = get_ncvardimlist(file_nc=file_nc)
    data_nc_NAMWL = get_hisstationlist(file_nc=file_nc, varname='NAMWL')
    #data_nc_NAMC = get_hisstationlist(file_nc=file_nc, varname='NAMC')
    data_nc_ZWL = get_ncmodeldata(file_nc=file_nc, varname='ZWL',timestep='all',station='all')
    #data_nc_ZCURU = get_ncmodeldata(file_nc=file_nc, varname='ZCURU',timestep='all',station='all')
    #data_nc_ZCURV = get_ncmodeldata(file_nc=file_nc, varname='ZCURV',timestep='all',station='all')

    fig, ax = plt.subplots(figsize=(16,7))
    for iS in range(10):
        ax.plot(data_nc_ZWL.var_times,data_nc_ZWL[:,iS],label=data_nc_NAMWL['NAMWL'].iloc[iS], linewidth=1)
    ax.legend(loc=1)
    ax.set_ylabel('%s (%s)'%(data_nc_ZWL.var_varname, data_nc_ZWL.var_ncvarobject.units))
    ax.set_xlim([data_nc_ZWL.var_times[0],data_nc_ZWL.var_times[0]+dt.timedelta(days=14)])
    plt.savefig(os.path.join(dir_output,'waqua_DSCM_his_ZWL'))
    
    
    #MAP OSR
    file_nc = r'p:\11205258-006-kpp2020_rmm-g6\C_Work\ZZ_Jelmer\SDS-nsctri_map.nc'
    vars_pd, dims_pd = get_ncvardimlist(file_nc=file_nc)
    
    data_nc_x = get_ncmodeldata(file_nc=file_nc, varname='grid_x')
    data_nc_y = get_ncmodeldata(file_nc=file_nc, varname='grid_y')
    data_nc_xcen = np.mean(data_nc_x, axis=2)
    data_nc_ycen = np.mean(data_nc_y, axis=2)
    
    timestep = 10
    data_nc_SEP = get_ncmodeldata(file_nc=file_nc, varname='SEP',timestep=timestep)
    data_nc_VELU = get_ncmodeldata(file_nc=file_nc, varname='VELU',timestep=timestep, layer=9)
    data_nc_VELV = get_ncmodeldata(file_nc=file_nc, varname='VELV',timestep=timestep, layer=9)
    
    fig, ax = plt.subplots()
    pc = ax.pcolor(data_nc_xcen,data_nc_ycen,data_nc_SEP[0,:,:],cmap='jet')
    pc.set_clim([0,2])
    cbar = fig.colorbar(pc, ax=ax)
    cbar.set_label('%s (%s)'%(data_nc_SEP.var_varname, data_nc_SEP.var_ncvarobject.units))
    ax.set_title('t=%d (%s)'%(timestep, data_nc_SEP.var_times.loc[timestep]))
    ax.set_aspect('equal')
    fig.tight_layout()
    plt.savefig(os.path.join(dir_output,'waqua_OSR_map_wl'))

    fig, ax = plt.subplots()
    vel_magn = np.sqrt(data_nc_VELU**2 + data_nc_VELV**2)
    pc = ax.pcolor(data_nc_xcen,data_nc_ycen,vel_magn[0,:,:,0],cmap='jet')
    pc.set_clim([0,1])
    cbar = fig.colorbar(pc, ax=ax)
    cbar.set_label('velocity magnitude (%s)'%(data_nc_VELU.var_ncvarobject.units))
    ax.set_title('t=%d (%s)'%(timestep, data_nc_VELU.var_times.loc[timestep]))
    ax.set_aspect('equal')
    thinning = 10
    ax.quiver(data_nc_xcen[::thinning,::thinning], data_nc_ycen[::thinning,::thinning], data_nc_VELU[0,::thinning,::thinning,0], data_nc_VELV[0,::thinning,::thinning,0], 
              color='w',scale=10)#,width=0.005)#, edgecolor='face', cmap='jet')
    ax.set_xlim([58000, 66000])
    ax.set_ylim([442000, 448000])
    fig.tight_layout()
    plt.savefig(os.path.join(dir_output,'waqua_OSR_map_vel'))
    
    #HIS OSR
    file_nc = r'p:\11205258-006-kpp2020_rmm-g6\C_Work\ZZ_Jelmer\SDS-nsctri_his.nc'
    vars_pd, dims_pd = get_ncvardimlist(file_nc=file_nc)
    data_nc_NAMWL = get_hisstationlist(file_nc=file_nc, varname='NAMWL')
    #data_nc_NAMC = get_hisstationlist(file_nc=file_nc, varname='NAMC')
    data_nc_ZWL = get_ncmodeldata(file_nc=file_nc, varname='ZWL',timestep='all',station='all')
    #data_nc_ZCURU = get_ncmodeldata(file_nc=file_nc, varname='ZCURU',timestep='all',station='all',layer='all')
    #data_nc_ZCURV = get_ncmodeldata(file_nc=file_nc, varname='ZCURV',timestep='all',station='all',layer='all')

    fig, ax = plt.subplots(figsize=(16,7))
    for iS in range(10):
        ax.plot(data_nc_ZWL.var_times,data_nc_ZWL[:,iS],label=data_nc_NAMWL['NAMWL'].iloc[iS], linewidth=1)
    ax.legend()
    ax.set_ylabel('%s (%s)'%(data_nc_ZWL.var_varname, data_nc_ZWL.var_ncvarobject.units))
    ax.set_xlim([data_nc_ZWL.var_times[0],data_nc_ZWL.var_times[0]+dt.timedelta(days=14)])
    plt.savefig(os.path.join(dir_output,'waqua_OSR_his_ZWL'))
    
    
    
    #MAP RMM
    RMM_names = ['RMM','RMMtestmodel']
    for RMM_name in RMM_names:
        if RMM_name=='RMM':
            file_nc_map = r'p:\11205258-006-kpp2020_rmm-g6\C_Work\07_WAQUAresultaten\j15\SDS-riv_tba_map.nc'
            file_nc_his = r'p:\11205258-006-kpp2020_rmm-g6\C_Work\07_WAQUAresultaten\j15\SDS-riv_tba_his.nc'
            timestep = 1
        elif RMM_name == 'RMMtestmodel':
            file_nc_map = r'c:\DATA\dfm_tools_testdata\waqua_netcdf\SDS-haven_map.nc'
            file_nc_his = r'c:\DATA\dfm_tools_testdata\waqua_netcdf\SDS-haven_his.nc'
            timestep = 10
    
        file_nc = file_nc_map
        vars_pd, dims_pd = get_ncvardimlist(file_nc=file_nc)
        
        data_nc_x = get_ncmodeldata(file_nc=file_nc, varname='grid_x')
        data_nc_y = get_ncmodeldata(file_nc=file_nc, varname='grid_y')
        data_nc_xcen = np.mean(data_nc_x, axis=2)
        data_nc_ycen = np.mean(data_nc_y, axis=2)
        
        data_nc_SEP = get_ncmodeldata(file_nc=file_nc, varname='SEP',timestep=timestep)
        data_nc_VELU = get_ncmodeldata(file_nc=file_nc, varname='VELU',timestep=timestep, layer=0)
        data_nc_VELV = get_ncmodeldata(file_nc=file_nc, varname='VELV',timestep=timestep, layer=0)
        
        fig, ax = plt.subplots(figsize=(16,7))
        pc = ax.pcolor(data_nc_xcen,data_nc_ycen,data_nc_SEP[0,:,:],cmap='jet')
        pc.set_clim([0,3])
        cbar = fig.colorbar(pc, ax=ax)
        cbar.set_label('%s (%s)'%(data_nc_SEP.var_varname, data_nc_SEP.var_ncvarobject.units))
        ax.set_title('t=%d (%s)'%(timestep, data_nc_SEP.var_times.loc[timestep]))
        ax.set_aspect('equal')
        fig.tight_layout()
        plt.savefig(os.path.join(dir_output,'waqua_%s_map_wl'%(RMM_name)))
    
        if RMM_name=='RMM':
            fig, ax = plt.subplots()
        else:
            fig, ax = plt.subplots(figsize=(16,7))
        vel_magn = np.sqrt(data_nc_VELU**2 + data_nc_VELV**2)
        pc = ax.pcolor(data_nc_xcen,data_nc_ycen,vel_magn[0,:,:,0],cmap='jet')
        pc.set_clim([0,1])
        cbar = fig.colorbar(pc, ax=ax)
        cbar.set_label('velocity magnitude (%s)'%(data_nc_VELU.var_ncvarobject.units))
        ax.set_title('t=%d (%s)'%(timestep, data_nc_VELU.var_times.loc[timestep]))
        ax.set_aspect('equal')
        if RMM_name=='RMM':
            thinning = 10
        else:
            thinning = 1
        ax.quiver(data_nc_xcen[::thinning,::thinning], data_nc_ycen[::thinning,::thinning], data_nc_VELU[0,::thinning,::thinning,0], data_nc_VELV[0,::thinning,::thinning,0], 
                  color='w',scale=10)#,width=0.005)#, edgecolor='face', cmap='jet')
        if RMM_name=='RMM':
            ax.set_xlim([61000, 72000])
            ax.set_ylim([438000, 446000])
        fig.tight_layout()
        plt.savefig(os.path.join(dir_output,'waqua_%s_map_vel'%(RMM_name)))
        
        #HIS RMM
        file_nc = file_nc_his
        vars_pd, dims_pd = get_ncvardimlist(file_nc=file_nc)
        data_nc_NAMWL = get_hisstationlist(file_nc=file_nc, varname='NAMWL')
        #data_nc_NAMC = get_hisstationlist(file_nc=file_nc, varname='NAMC')
        data_nc_ZWL = get_ncmodeldata(file_nc=file_nc, varname='ZWL',timestep='all',station='all')
        #data_nc_ZCURU = get_ncmodeldata(file_nc=file_nc, varname='ZCURU',timestep='all',station='all',layer='all')
        #data_nc_ZCURV = get_ncmodeldata(file_nc=file_nc, varname='ZCURV',timestep='all',station='all',layer='all')
    
        fig, ax = plt.subplots(figsize=(16,7))
        for iS in range(10):
            ax.plot(data_nc_ZWL.var_times,data_nc_ZWL[:,iS],label=data_nc_NAMWL['NAMWL'].iloc[iS], linewidth=1)
        ax.legend()
        ax.set_ylabel('%s (%s)'%(data_nc_ZWL.var_varname, data_nc_ZWL.var_ncvarobject.units))
        if RMM_name=='RMM':
            ax.set_xlim([data_nc_ZWL.var_times[0],data_nc_ZWL.var_times[0]+dt.timedelta(days=14)])
        plt.savefig(os.path.join(dir_output,'waqua_%s_his_ZWL'%(RMM_name)))








@pytest.mark.acceptance
def test_contour_over_polycollection():
    dir_output = getmakeoutputdir(__file__,inspect.currentframe().f_code.co_name)
    """
    dir_output = './test_output'
    file_nc = os.path.join(dir_testinput,'DFM_sigma_curved_bend\\DFM_OUTPUT_cb_3d\\cb_3d_map.nc')
    file_nc = os.path.join(dir_testinput,'DFM_3D_z_Grevelingen','computations','run01','DFM_OUTPUT_Grevelingen-FM','Grevelingen-FM_0000_map.nc')
    file_nc = 'p:\\1204257-dcsmzuno\\2013-2017\\3D-DCSM-FM\\A17b\\DFM_OUTPUT_DCSM-FM_0_5nm\\DCSM-FM_0_5nm_0000_map.nc'
    file_nc = 'p:\\11205258-006-kpp2020_rmm-g6\\C_Work\\08_RMM_FMmodel\\computations\\run_156\\DFM_OUTPUT_RMM_dflowfm\\RMM_dflowfm_0000_map.nc'
    """
    
    import matplotlib.pyplot as plt
    plt.close('all')
    
    from dfm_tools.get_nc import get_netdata, get_ncmodeldata, plot_netmapdata
    from dfm_tools.get_nc_helpers import get_ncvardimlist
    from dfm_tools.regulargrid import scatter_to_regulargrid
    
    file_nc = os.path.join(dir_testinput,'DFM_3D_z_Grevelingen','computations','run01','DFM_OUTPUT_Grevelingen-FM','Grevelingen-FM_0000_map.nc')
    
    clim_bl = [-40,10]

    vars_pd, dims_pd = get_ncvardimlist(file_nc=file_nc)
    ugrid = get_netdata(file_nc=file_nc)
    #get bed layer
    data_frommap_x = get_ncmodeldata(file_nc=file_nc, varname='mesh2d_face_x')
    data_frommap_y = get_ncmodeldata(file_nc=file_nc, varname='mesh2d_face_y')
    data_frommap_bl = get_ncmodeldata(file_nc=file_nc, varname='mesh2d_flowelem_bl')
    
    for maskland_dist in [None,100]:
        #interpolate to regular grid
        x_grid, y_grid, val_grid = scatter_to_regulargrid(xcoords=data_frommap_x, ycoords=data_frommap_y, ncellx=100, ncelly=80, values=data_frommap_bl, method='linear', maskland_dist=maskland_dist)
    
        #create plot with ugrid and cross section line
        fig, axs = plt.subplots(3,1,figsize=(6,9))
        ax=axs[0]
        pc = plot_netmapdata(ugrid.verts, values=data_frommap_bl, ax=ax, linewidth=0.5, edgecolors='face', cmap='jet')#, color='crimson', facecolor="None")
        pc.set_clim(clim_bl)
        fig.colorbar(pc, ax=ax)
        ax=axs[1]
        pc = ax.contourf(x_grid, y_grid, val_grid)
        pc.set_clim(clim_bl)
        fig.colorbar(pc, ax=ax)
        ax=axs[2]
        ax.contour(x_grid, y_grid, val_grid)
        fig.colorbar(pc, ax=ax)
        plt.savefig(os.path.join(dir_output,'%s_gridbedcontour_masklanddist%s'%(os.path.basename(file_nc).replace('.',''),maskland_dist)))







@pytest.mark.acceptance
def test_morphology():
    dir_output = getmakeoutputdir(__file__,inspect.currentframe().f_code.co_name)
    """
    dir_output = './test_output'
    """
    
    import matplotlib.pyplot as plt
    plt.close('all')
    import numpy as np
    #import datetime as dt

    from dfm_tools.get_nc import get_netdata, get_ncmodeldata, plot_netmapdata#, get_xzcoords_onintersection
    from dfm_tools.get_nc_helpers import get_ncvardimlist, get_hisstationlist
    from dfm_tools.regulargrid import scatter_to_regulargrid#, meshgridxy2verts, center2corner
    
    #MAPFILE
    file_nc = r'p:\11203869-morwaqeco3d\05-Tidal_inlet\02_FM_201910\FM_MF10_Max_30s\fm\DFM_OUTPUT_inlet\inlet_map.nc'
    vars_pd, dims_pd = get_ncvardimlist(file_nc=file_nc)
    vars_pd.to_csv(os.path.join(dir_output,'vars_pd.csv'))
    vars_pd_sel = vars_pd[vars_pd['long_name'].str.contains('transport')]
    #vars_pd_sel = vars_pd[vars_pd['dimensions'].str.contains('mesh2d_nFaces') & vars_pd['long_name'].str.contains('wave')]
    
    ugrid = get_netdata(file_nc=file_nc)

    varname = 'mesh2d_mor_bl'
    var_clims = [-50,0]
    var_longname = vars_pd['long_name'][vars_pd['nc_varkeys']==varname].iloc[0]
    fig, axs = plt.subplots(3,1, figsize=(6,9))
    fig.suptitle('%s (%s)'%(varname, var_longname))
    
    ax = axs[0]
    data_frommap_0 = get_ncmodeldata(file_nc=file_nc, varname=varname, timestep=0, get_linkedgridinfo=True)
    pc = plot_netmapdata(ugrid.verts, values=data_frommap_0.flatten(), ax=ax, linewidth=0.5, cmap='jet', clim=var_clims)
    cbar = fig.colorbar(pc, ax=ax)
    cbar.set_label('%s (%s)'%(data_frommap_0.var_varname, data_frommap_0.var_ncvarobject.units))
    ax.set_title('t=0 (%s)'%(data_frommap_0.var_times.iloc[0]))
    
    ax = axs[1]
    data_frommap_end = get_ncmodeldata(file_nc=file_nc, varname=varname, timestep=-1)
    pc = plot_netmapdata(ugrid.verts, values=data_frommap_end.flatten(), ax=ax, linewidth=0.5, cmap='jet', clim=var_clims)
    cbar = fig.colorbar(pc, ax=ax)
    cbar.set_label('%s (%s)'%(data_frommap_end.var_varname, data_frommap_end.var_ncvarobject.units))
    ax.set_title('t=end (%s)'%(data_frommap_end.var_times.iloc[0]))
    
    ax = axs[2]
    pc = plot_netmapdata(ugrid.verts, values=(data_frommap_end-data_frommap_0).flatten(), ax=ax, linewidth=0.5, cmap='jet', clim=[-3,3])
    cbar = fig.colorbar(pc, ax=ax)
    cbar.set_label('%s (%s)'%(data_frommap_0.var_varname, data_frommap_0.var_ncvarobject.units))
    ax.set_title('t=end-0 (difference)')

    for ax in axs:
        ax.set_aspect('equal')
        #ax.set_ylim(val_ylim)
    fig.tight_layout()
    plt.savefig(os.path.join(dir_output,'%s_%s'%(os.path.basename(file_nc).replace('.',''), varname)))



    varname = 'mesh2d_hwav'
    var_longname = vars_pd['long_name'][vars_pd['nc_varkeys']==varname].iloc[0]
    fig, ax = plt.subplots(1,1)
    fig.suptitle('%s (%s)'%(varname, var_longname))
    
    data_frommap = get_ncmodeldata(file_nc=file_nc, varname=varname, timestep=-1)
    pc = plot_netmapdata(ugrid.verts, values=data_frommap.flatten(), ax=ax, linewidth=0.5, cmap='jet')
    cbar = fig.colorbar(pc, ax=ax)
    cbar.set_label('%s (%s)'%(data_frommap.var_varname, data_frommap.var_ncvarobject.units))
    ax.set_title('t=end (%s)'%(data_frommap.var_times.iloc[0]))
    ax.set_aspect('equal')

    fig.tight_layout()
    plt.savefig(os.path.join(dir_output,'%s_%s'%(os.path.basename(file_nc).replace('.',''), varname)))

    
    
    
    #file_nc = r'p:\11203869-morwaqeco3d\05-Tidal_inlet\02_FM_201910\FM_MF10_Max_30s\fm\DFM_OUTPUT_inlet\inlet_com.nc'
    """
    #COMFILE
    vars_pd, dims_pd = get_ncvardimlist(file_nc=file_nc)
    vars_pd_sel = vars_pd[vars_pd['long_name'].str.contains('wave')]
    #vars_pd_sel = vars_pd[vars_pd['dimensions'].str.contains('mesh2d_nFaces') & vars_pd['long_name'].str.contains('wave')]
    
    ugrid = get_netdata(file_nc=file_nc)
    
    #construct different ugrid (with bnds?)
    data_fromnc_FlowElemContour_x = get_ncmodeldata(file_nc=file_nc, varname='FlowElemContour_x')
    data_fromnc_FlowElemContour_y = get_ncmodeldata(file_nc=file_nc, varname='FlowElemContour_y')
    data_fromnc_FlowElemContour_xy = np.stack([data_fromnc_FlowElemContour_x,data_fromnc_FlowElemContour_y],axis=2)

    varname_list = ['hrms', 'tp', 'dir']#, 'distot', 'wlen']
    for varname in varname_list:
        var_longname = vars_pd['long_name'][vars_pd['nc_varkeys']==varname].iloc[0]
        fig, ax = plt.subplots()#fig, axs = plt.subplots(2,1, figsize=(6,8))
        fig.suptitle('%s (%s)'%(varname, var_longname))
        
        timestep = 0
        data_frommap = get_ncmodeldata(file_nc=file_nc, varname=varname, timestep=timestep)
        pc = plot_netmapdata(data_fromnc_FlowElemContour_xy, values=data_frommap.flatten(), ax=ax, linewidth=0.5, cmap='jet')
        cbar = fig.colorbar(pc, ax=ax)
        cbar.set_label('%s (%s)'%(data_frommap.var_varname, data_frommap.var_ncvarobject.units))
        ax.set_title('t=%d (%s)'%(timestep, data_frommap.var_times.iloc[0]))
        ax.set_aspect('equal')
        
        fig.tight_layout()
        plt.savefig(os.path.join(dir_output,'%s_%s'%(os.path.basename(file_nc).replace('.',''), varname)))
    """

    #WAVM FILE
    file_nc = r'p:\11203869-morwaqeco3d\05-Tidal_inlet\02_FM_201910\FM_MF10_Max_30s\wave\wavm-inlet.nc'
    vars_pd, dims_pd = get_ncvardimlist(file_nc=file_nc)
    vars_pd_sel = vars_pd[vars_pd['long_name'].str.contains('dissi')]
    #vars_pd_sel = vars_pd[vars_pd['dimensions'].str.contains('mesh2d_nFaces') & vars_pd['long_name'].str.contains('wave')]
    
    
    #get cell center coordinates from regular grid, convert to grid_verts on corners
    data_fromnc_x = get_ncmodeldata(file_nc=file_nc, varname='x')
    data_fromnc_y = get_ncmodeldata(file_nc=file_nc, varname='y')
    #x_cen_withbnd = center2corner(data_fromnc_x)
    #y_cen_withbnd = center2corner(data_fromnc_y)
    #grid_verts = meshgridxy2verts(x_cen_withbnd, y_cen_withbnd)

    #plt.close('all')
    varname_list = ['hsign', 'dir', 'period', 'dspr', 'dissip']
    var_clim = [[0,2], [0,360], [0,7.5], [0,35], [0,20]]
    for iV, varname in enumerate(varname_list):
        var_longname = vars_pd['long_name'][vars_pd['nc_varkeys']==varname].iloc[0]
        
        fig, axs = plt.subplots(2,1, figsize=(12,7))
        fig.suptitle('%s (%s)'%(varname, var_longname))

        timestep = 10
        data_frommap = get_ncmodeldata(file_nc=file_nc, varname=varname, timestep=timestep, get_linkedgridinfo=True)
        ax = axs[0]
        pc = ax.pcolor(data_fromnc_x, data_fromnc_y, data_frommap[0,:,:], cmap='jet')
        pc.set_clim(var_clim[iV])
        cbar = fig.colorbar(pc, ax=ax)
        cbar.set_label('%s (%s)'%(data_frommap.var_varname, data_frommap.var_ncvarobject.units))
        ax.set_title('t=%d (%s)'%(timestep, data_frommap.var_times.iloc[0]))
        ax.set_aspect('equal')
        
        timestep = -1
        data_frommap = get_ncmodeldata(file_nc=file_nc, varname=varname, timestep=timestep)        
        ax = axs[1]
        pc = ax.pcolor(data_fromnc_x, data_fromnc_y, data_frommap[0,:,:], cmap='jet')
        pc.set_clim(var_clim[iV])
        cbar = fig.colorbar(pc, ax=ax)
        cbar.set_label('%s (%s)'%(data_frommap.var_varname, data_frommap.var_ncvarobject.units))
        ax.set_title('t=%d (%s)'%(timestep, data_frommap.var_times.iloc[0]))
        ax.set_aspect('equal')
        
        fig.tight_layout()
        plt.savefig(os.path.join(dir_output,'%s_%s'%(os.path.basename(file_nc).replace('.',''), varname)))
        
        if varname == 'dir':
            #also plot with vectors
            ax = axs[0]
            ax.clear()
            pc = ax.quiver(data_fromnc_x, data_fromnc_y, 1,1,data_frommap[0,:,:],
                           angles=90-data_frommap[0,:,:], cmap='jet', scale=100)
            for ax in axs:
                ax.set_title('t=%d (%s)'%(timestep, data_frommap.var_times.iloc[0]))
                ax.set_aspect('equal')
            plt.savefig(os.path.join(dir_output,'%s_%s_vec'%(os.path.basename(file_nc).replace('.',''), varname)))
            for ax in axs:
                ax.set_xlim([25000,65000])
                ax.set_ylim([2500,15000])
            plt.savefig(os.path.join(dir_output,'%s_%s_veczoom'%(os.path.basename(file_nc).replace('.',''), varname)))
    
    
    
    #HISFILE
    file_nc = r'p:\11203869-morwaqeco3d\05-Tidal_inlet\02_FM_201910\FM_MF10_Max_30s\fm\DFM_OUTPUT_inlet\inlet_his.nc'
    vars_pd, dims_pd = get_ncvardimlist(file_nc=file_nc)
    vars_pd_sel = vars_pd[vars_pd['long_name'].str.contains('level')]
    stat_list = get_hisstationlist(file_nc,varname='station_name')
    crs_list = get_hisstationlist(file_nc,varname='cross_section_name')
    
    var_names = ['waterlevel','bedlevel']#,'mesh2d_ssn']
    for iV, varname in enumerate(var_names):
        data_fromhis = get_ncmodeldata(file_nc=file_nc, varname=varname, timestep='all', station='all')
        var_longname = vars_pd['long_name'][vars_pd['nc_varkeys']==varname].iloc[0]
    
        fig, ax = plt.subplots(1,1, figsize=(10,5))
        for iS, stat in enumerate(data_fromhis.var_stations['station_name']):
            ax.plot(data_fromhis.var_times, data_fromhis[:,iS], linewidth=1, label=stat)
        ax.legend()
        ax.set_ylabel('%s (%s)'%(data_fromhis.var_varname,data_fromhis.var_ncvarobject.units))
        ax.set_xlim(data_fromhis.var_times[[0,3000]])
        fig.tight_layout()
        plt.savefig(os.path.join(dir_output,'%s_%s'%(os.path.basename(file_nc).replace('.',''), varname)))
    
    
    
    
    
    
    #MAPFILE TRANSPORT
    file_nc = r'p:\11203869-morwaqeco3d\05-Tidal_inlet\02_FM_201910\FM_MF10_Max_30s\fm\DFM_OUTPUT_inlet\inlet_map.nc'
    #file_nc = r'p:\11203869-morwaqeco3d\04-Breakwater\02_FM_201910\01_FM_MF25_Max_30s_User_1200s\fm\DFM_OUTPUT_straight_coast\straight_coast_map.nc'
    vars_pd, dims_pd = get_ncvardimlist(file_nc=file_nc)
    #vars_pd_sel = vars_pd[vars_pd['long_name'].str.contains('transport')]
    #vars_pd_sel = vars_pd[vars_pd['dimensions'].str.contains('mesh2d_nFaces') & vars_pd['long_name'].str.contains('wave')]
    
    ugrid = get_netdata(file_nc=file_nc)
    timestep = 10
    data_frommap_facex = get_ncmodeldata(file_nc=file_nc, varname='mesh2d_face_x')
    data_frommap_facey = get_ncmodeldata(file_nc=file_nc, varname='mesh2d_face_y')
    data_frommap_transx = get_ncmodeldata(file_nc=file_nc, varname='mesh2d_sxtot', timestep=timestep, station='all')
    data_frommap_transy = get_ncmodeldata(file_nc=file_nc, varname='mesh2d_sytot', timestep=timestep, station='all')
    magnitude = (data_frommap_transx ** 2 + data_frommap_transy ** 2) ** 0.5
    
    #plt.close('all')
    fig, ax = plt.subplots(1,1, figsize=(14,8))
    quiv = ax.quiver(data_frommap_facex, data_frommap_facey, data_frommap_transx[0,0,:], data_frommap_transy[0,0,:],
                     magnitude[0,0,:])#, scale=0.015)
    cbar = fig.colorbar(quiv, ax=ax)
    cbar.set_label('%s and %s (%s)'%(data_frommap_transx.var_varname, data_frommap_transy.var_varname, data_frommap_transy.var_ncvarobject.units))
    ax.set_title('t=%d (%s)'%(timestep, data_frommap_transx.var_times.iloc[0]))
    ax.set_aspect('equal')
    fig.tight_layout()
    plt.savefig(os.path.join(dir_output,'%s_%s_%s_t%d'%(os.path.basename(file_nc).replace('.',''), data_frommap_transx.var_varname, data_frommap_transy.var_varname,timestep)))
    xlim_get = ax.get_xlim()
    ylim_get = ax.get_ylim()
    
    #interpolate to regular grid
    X,Y,U = scatter_to_regulargrid(xcoords=data_frommap_facex, ycoords=data_frommap_facey, ncellx=29, ncelly=20, values=data_frommap_transx[0,0,:])
    X,Y,V = scatter_to_regulargrid(xcoords=data_frommap_facex, ycoords=data_frommap_facey, ncellx=29, ncelly=20, values=data_frommap_transy[0,0,:])
    speed = np.sqrt(U*U + V*V)
    
    fig, ax = plt.subplots(1,1, figsize=(14,8))
    quiv = ax.quiver(X, Y, U, V, speed)
    cbar = fig.colorbar(quiv, ax=ax)
    cbar.set_label('%s and %s (%s)'%(data_frommap_transx.var_varname, data_frommap_transy.var_varname, data_frommap_transy.var_ncvarobject.units))
    ax.set_title('t=%d (%s)'%(timestep, data_frommap_transx.var_times.iloc[0]))
    ax.set_xlim(xlim_get)
    ax.set_ylim(ylim_get)
    ax.set_aspect('equal')
    fig.tight_layout()
    plt.savefig(os.path.join(dir_output,'%s_%s_%s_t%d_regquiver'%(os.path.basename(file_nc).replace('.',''), data_frommap_transx.var_varname, data_frommap_transy.var_varname,timestep)))

    #xs = X.flatten()
    #ys = Y.flatten()
    #seed_points = np.array([list(xs), list(ys)])
    fig, ax = plt.subplots(1,1, figsize=(14,8))
    strm = ax.streamplot(X, Y, U, V, color=speed, density=2, linewidth=1+2*speed/np.max(speed))#, cmap='winter', 
    #                      minlength=0.01, maxlength = 2, arrowstyle='fancy')#,
    #                      integration_direction='forward')#, start_points = seed_points.T)
    #strm = ax.streamplot(X, Y, U, V, color=speed, linewidth=1+2*speed/np.max(speed), density=10,# cmap='winter',
    #                     minlength=0.0001, maxlength = 0.07, arrowstyle='fancy',
    #                     integration_direction='forward', start_points = seed_points.T)
    cbar = fig.colorbar(strm.lines)
    cbar.set_label('%s and %s (%s)'%(data_frommap_transx.var_varname, data_frommap_transy.var_varname, data_frommap_transy.var_ncvarobject.units))
    ax.set_title('t=%d (%s)'%(timestep, data_frommap_transx.var_times.iloc[0]))
    ax.set_xlim(xlim_get)
    ax.set_ylim(ylim_get)
    ax.set_aspect('equal')
    fig.tight_layout()
    plt.savefig(os.path.join(dir_output,'%s_%s_%s_t%d_regstreamplot'%(os.path.basename(file_nc).replace('.',''), data_frommap_transx.var_varname, data_frommap_transy.var_varname,timestep)))
    
    from dfm_tools.modplot import velovect
    fig, ax = plt.subplots(1,1, figsize=(14,8))
    quiv_curved = velovect(ax,X,Y,U,V, arrowstyle='fancy', scale = 5, grains = 25, color=speed)
    cbar = fig.colorbar(quiv_curved.lines)
    cbar.set_label('%s and %s (%s)'%(data_frommap_transx.var_varname, data_frommap_transy.var_varname, data_frommap_transy.var_ncvarobject.units))
    ax.set_title('t=%d (%s)'%(timestep, data_frommap_transx.var_times.iloc[0]))
    ax.set_xlim(xlim_get)
    ax.set_ylim(ylim_get)
    ax.set_aspect('equal')
    fig.tight_layout()
    plt.savefig(os.path.join(dir_output,'%s_%s_%s_t%d_curvedquiver'%(os.path.basename(file_nc).replace('.',''), data_frommap_transx.var_varname, data_frommap_transy.var_varname,timestep)))

    






@pytest.mark.acceptance
def test_workinprogress():
    ## WARNING: THIS TEST IS NOT YET FINISHED, WILL BE IMPROVED AND LINKED TO INTERNAL FUNCTIONS ASAP
    dir_output = getmakeoutputdir(__file__,inspect.currentframe().f_code.co_name)
    """
    dir_output = './test_output'
    """
    
    import os
    import matplotlib.pyplot as plt
    import numpy as np
    plt.close('all')
    
    from dfm_tools.get_nc import get_netdata, get_ncmodeldata, plot_netmapdata
    from dfm_tools.get_nc_helpers import get_ncvardimlist, get_hisstationlist#, get_varname_fromnc
    from dfm_tools.io.polygon import Polygon
    
    #print gridinfo of several files to compare
    file_nc = r'p:\1204257-dcsmzuno\2014\data\meteo\HIRLAM72_2018\h72_201803.nc'
    print('\nfile = %s'%(file_nc))
    data_dummy = get_ncmodeldata(file_nc=file_nc, varname='northward_wind', timestep=0, get_linkedgridinfo=True)
    file_nc = r'p:\1220688-lake-kivu\2_data\COSMO\COSMOCLM_2012_out02_merged_4Wouter.nc'
    print('\nfile = %s'%(file_nc))
    data_dummy = get_ncmodeldata(file_nc=file_nc, varname='U_10M', timestep=0, get_linkedgridinfo=True)
    file_nc = r'p:\11200665-c3s-codec\2_Hydro\ECWMF_meteo\meteo\ERA-5\2000\ERA5_metOcean_atm_19991201_19991231.nc'
    print('\nfile = %s'%(file_nc))
    data_dummy = get_ncmodeldata(file_nc=file_nc, varname='msl', timestep=0, get_linkedgridinfo=True)
    file_nc = r'p:\11202255-sfincs\Testbed\Original_runs\01_Implementation\08_restartfile\sfincs_map.nc'
    print('\nfile = %s'%(file_nc))
    data_dummy = get_ncmodeldata(file_nc=file_nc, varname='zs', timestep=0, get_linkedgridinfo=True)
    print('\nfile = %s'%(file_nc))
    data_dummy = get_ncmodeldata(file_nc=file_nc, varname='u', timestep=0, get_linkedgridinfo=True)
    file_nc = r'p:\1220688-lake-kivu\3_modelling\1_FLOW\7_heatfluxinhis\063_netcdf\trim-thiery_002_coarse.nc'
    print('\nfile = %s'%(file_nc))
    data_dummy = get_ncmodeldata(file_nc=file_nc, varname='S1', timestep=0, get_linkedgridinfo=True)
    print('\nfile = %s'%(file_nc))
    data_dummy = get_ncmodeldata(file_nc=file_nc, varname='U1', timestep=0, layer=0, get_linkedgridinfo=True)
    print('\nfile = %s'%(file_nc))
    data_dummy = get_ncmodeldata(file_nc=file_nc, varname='V1', timestep=0, layer=0, get_linkedgridinfo=True)
    file_nc = r'p:\1204257-dcsmzuno\2019\DCSMv6\A01\SDS-A01_map.nc'
    print('\nfile = %s'%(file_nc))
    data_dummy = get_ncmodeldata(file_nc=file_nc, varname='SEP', timestep=0, get_linkedgridinfo=True)
    print('\nfile = %s'%(file_nc))
    data_dummy = get_ncmodeldata(file_nc=file_nc, varname='VELU', timestep=0, layer=0, get_linkedgridinfo=True)
    file_nc = r'p:\11203869-morwaqeco3d\05-Tidal_inlet\02_FM_201910\FM_MF10_Max_30s\wave\wavm-inlet.nc'
    print('\nfile = %s'%(file_nc))
    data_dummy = get_ncmodeldata(file_nc=file_nc, varname='veloc-x', timestep=0, get_linkedgridinfo=True)
    file_nc = os.path.join(dir_testinput,r'DFM_3D_z_Grevelingen\computations\run01\DFM_OUTPUT_Grevelingen-FM\Grevelingen-FM_0000_map.nc')
    print('\nfile = %s'%(file_nc))
    data_dummy = get_ncmodeldata(file_nc=file_nc, varname='mesh2d_s1', timestep=0, multipart=False, get_linkedgridinfo=True)
    data_dummy = get_ncmodeldata(file_nc=file_nc, varname='mesh2d_u1', timestep=0, layer=0, multipart=False, get_linkedgridinfo=True)
    data_dummy = get_ncmodeldata(file_nc=file_nc, varname='mesh2d_flowelem_bl', multipart=False, get_linkedgridinfo=True)
    
    
    # test Grevelingen (integrated example, where all below should move towards)
    file_nc = os.path.join(dir_testinput,r'DFM_3D_z_Grevelingen\computations\run01\DFM_OUTPUT_Grevelingen-FM\Grevelingen-FM_0000_map.nc')
    vars_pd, dims_pd = get_ncvardimlist(file_nc=file_nc)
    ugrid = get_netdata(file_nc=file_nc)
    fig, ax = plt.subplots()
    plot_netmapdata(ugrid.verts, values=None, ax=None, linewidth=0.5, color="crimson", facecolor="None")
    ax.set_aspect('equal')
    
    #hirlam
    file_nc = r'p:\1204257-dcsmzuno\2014\data\meteo\HIRLAM72_2018\h72_201803.nc'
    vars_pd, dims_pd = get_ncvardimlist(file_nc=file_nc)
    
    mesh2d_node_x = get_ncmodeldata(file_nc=file_nc, varname='x')
    mesh2d_node_y = get_ncmodeldata(file_nc=file_nc, varname='y')
    data_v = get_ncmodeldata(file_nc=file_nc, varname='northward_wind',timestep=0, get_linkedgridinfo=True)
    data_u = get_ncmodeldata(file_nc=file_nc, varname='eastward_wind',timestep=0, get_linkedgridinfo=True)
    #airp = get_ncmodeldata(file_nc=file_nc, varname='air_pressure_fixed_height',timestep=0)[0,:,:]
    magn = np.sqrt(data_u[0,:,:]**2 + data_v[0,:,:]**2)
    
    fig, ax = plt.subplots()
    ax.plot(mesh2d_node_x,mesh2d_node_y,'-b',linewidth=0.2)
    ax.plot(mesh2d_node_x.T,mesh2d_node_y.T,'-b',linewidth=0.2)
    plt.savefig(os.path.join(dir_output,'hirlam_mesh'))

    
    fig, ax = plt.subplots()
    ax.pcolor(mesh2d_node_x,mesh2d_node_y,magn)
    #plt.pcolor(mesh2d_node_x,mesh2d_node_y,airp,linewidth=0.5)
    plt.savefig(os.path.join(dir_output,'hirlam_magn_pcolor'))
    
    
    #plt.close('all')
    from dfm_tools.regulargrid import center2corner
    #COSMO
    file_nc = r'p:\1220688-lake-kivu\2_data\COSMO\COSMOCLM_2012_out02_merged_4Wouter.nc'
    vars_pd, dims_pd = get_ncvardimlist(file_nc=file_nc)
    
    xcen = get_ncmodeldata(file_nc=file_nc, varname='lon')
    ycen = get_ncmodeldata(file_nc=file_nc, varname='lat')
    xcor = center2corner(xcen)
    ycor = center2corner(ycen)
    data_U10M = get_ncmodeldata(file_nc=file_nc, varname='U_10M', timestep=range(20), get_linkedgridinfo=True)
    data_V10M = get_ncmodeldata(file_nc=file_nc, varname='V_10M', timestep=range(20), get_linkedgridinfo=True)
    #xcen, ycen = np.meshgrid(data_lon, data_lat)
    magn = np.sqrt(data_U10M**2 + data_V10M**2)

    fig, ax = plt.subplots()
    ax.plot(xcen, ycen, '-b', linewidth=0.2)
    ax.plot(xcen.T, ycen.T, '-b', linewidth=0.2)
    plt.savefig(os.path.join(dir_output,'COSMO_mesh'))

    file_ldb = r'p:\1220688-lake-kivu\3_modelling\1_FLOW\4_CH4_CO2_included\008\lake_kivu_geo.ldb'
    data_ldb = Polygon.fromfile(file_ldb, pd_output=True)
    
    fig, axs = plt.subplots(1,3, figsize=(16,6))
    for iT, timestep in enumerate([0,1,10]):
        ax=axs[iT]
        #pc = ax.pcolor(xcen, ycen, magn[timestep,:,:], cmap='jet')
        pc = ax.pcolor(xcor, ycor, magn[timestep,:,:], cmap='jet')
        pc.set_clim([0,5])
        cbar = fig.colorbar(pc, ax=ax)
        cbar.set_label('velocity magnitude (%s)'%(data_V10M.var_ncvarobject.units))
        ax.set_title('t=%d (%s)'%(timestep, data_V10M.var_times.loc[timestep]))
        ax.set_aspect('equal')
        ax.plot(data_ldb[0].loc[:,0], data_ldb[0].loc[:,1], 'k', linewidth=0.5)
        thinning = 2
        ax.quiver(xcen[::thinning,::thinning], ycen[::thinning,::thinning], data_U10M[timestep,::thinning,::thinning], data_V10M[timestep,::thinning,::thinning], 
                  color='w',scale=50,width=0.008)#, edgecolor='face', cmap='jet')
    fig.tight_layout()
    plt.savefig(os.path.join(dir_output,'COSMO_magn_pcolorquiver'))



    dist = 0.1
    reg_x_vec = np.linspace(np.min(xcen),np.max(xcen),int(np.ceil((np.max(xcen)-np.min(xcen))/dist)))
    reg_y_vec = np.linspace(np.min(ycen),np.max(ycen),int(np.ceil((np.max(ycen)-np.min(ycen))/dist)))
    reg_grid = np.meshgrid(reg_x_vec,reg_y_vec)
    X = reg_grid[0]
    Y = reg_grid[1]
    from scipy.interpolate import griddata
    from dfm_tools.modplot import velovect
    
    fig, axs = plt.subplots(1,3, figsize=(16,6))
    for iT, timestep in enumerate([0,1,10]):
        ax=axs[iT]
        #pc = ax.pcolor(xcen, ycen, magn[timestep,:,:], cmap='jet')
        #pc.set_clim([0,5])
        U = griddata((xcen.flatten(),ycen.flatten()),data_U10M[timestep,:,:].flatten(),tuple(reg_grid),method='nearest')
        V = griddata((xcen.flatten(),ycen.flatten()),data_V10M[timestep,:,:].flatten(),tuple(reg_grid),method='nearest')
        speed = np.sqrt(U*U + V*V)
        quiv_curved = velovect(ax,X,Y,U,V, arrowstyle='fancy', scale = 5, grains = 25, color=speed)#, cmap='jet')
        ax.set_aspect('equal')
        cbar = fig.colorbar(quiv_curved.lines, ax=ax)
        cbar.set_label('velocity magnitude (%s)'%(data_V10M.var_ncvarobject.units))
        ax.set_title('t=%d (%s)'%(timestep, data_V10M.var_times.loc[timestep]))
        ax.set_aspect('equal')
        ax.plot(data_ldb[0].loc[:,0], data_ldb[0].loc[:,1], 'k', linewidth=0.5)
        thinning = 2
        ax.quiver(xcen[::thinning,::thinning], ycen[::thinning,::thinning], data_U10M[timestep,::thinning,::thinning], data_V10M[timestep,::thinning,::thinning], 
                  color='w',scale=50,width=0.008)#, edgecolor='face', cmap='jet')
    fig.tight_layout()
    plt.savefig(os.path.join(dir_output,'COSMO_magn_curvedquiver'))



    #ERA5
    file_nc = r'p:\11200665-c3s-codec\2_Hydro\ECWMF_meteo\meteo\ERA-5\2000\ERA5_metOcean_atm_19991201_19991231.nc'
    vars_pd, dims_pd = get_ncvardimlist(file_nc=file_nc)
    data_lon = get_ncmodeldata(file_nc=file_nc, varname='longitude')
    data_lat = get_ncmodeldata(file_nc=file_nc, varname='latitude')
    data_psl = get_ncmodeldata(file_nc=file_nc, varname='msl',timestep=10, get_linkedgridinfo=True)
    
    lons,lats = np.meshgrid(data_lon,data_lat)
    fig, ax = plt.subplots()
    ax.plot(lons, lats,'-b',linewidth=0.2)
    ax.plot(lons.T, lats.T,'-b',linewidth=0.2)
    plt.savefig(os.path.join(dir_output,'ERA5_mesh'))

    fig, ax = plt.subplots()
    #ax.pcolor(lons, lats, data_psl[0,:,:])
    ax.pcolor(data_lon, data_lat, data_psl[0,:,:])
    #plt.pcolor(mesh2d_node_x,mesh2d_node_y,airp,linewidth=0.5)
    plt.savefig(os.path.join(dir_output,'ERA5_msl_pcolor'))






    #SFINCS
    file_nc = r'p:\11202255-sfincs\Testbed\Original_runs\01_Implementation\08_restartfile\sfincs_map.nc'
    #file_nc = r'p:\11202255-sfincs\Testbed\Original_runs\03_Application\22_Tsunami_Japan_Sendai\sfincs_map.nc'
    vars_pd, dims_pd = get_ncvardimlist(file_nc=file_nc)
    
    data_fromnc_x = get_ncmodeldata(file_nc=file_nc, varname='x')
    data_fromnc_y = get_ncmodeldata(file_nc=file_nc, varname='y')
    data_fromnc_zs = get_ncmodeldata(file_nc=file_nc, varname='zs', timestep='all', get_linkedgridinfo=True)

    fig, ax = plt.subplots()
    ax.plot(data_fromnc_x, data_fromnc_y,'-b',linewidth=0.2)
    ax.plot(data_fromnc_x.T, data_fromnc_y.T,'-b',linewidth=0.2)
    plt.savefig(os.path.join(dir_output,'SFINCS_mesh'))    

    fig, axs = plt.subplots(3,1, figsize=(14,9))
    for iT, timestep in enumerate([0,1,10]):
        ax=axs[iT]
        pc = ax.pcolor(data_fromnc_x, data_fromnc_y, data_fromnc_zs[timestep,:,:],cmap='jet')
        pc.set_clim([0,0.15])
        cbar = fig.colorbar(pc, ax=ax)
        cbar.set_label('%s (%s)'%(data_fromnc_zs.var_varname, data_fromnc_zs.var_ncvarobject.units))
        ax.set_title('t=%d (%s)'%(timestep, data_fromnc_zs.var_times.loc[timestep]))
        ax.set_aspect('equal')
    fig.tight_layout()
    plt.savefig(os.path.join(dir_output,'SFINCS_zs_pcolor'))


    data_fromnc_edgex = get_ncmodeldata(file_nc=file_nc, varname='edge_x')
    data_fromnc_edgey = get_ncmodeldata(file_nc=file_nc, varname='edge_y')
    data_fromnc_u = get_ncmodeldata(file_nc=file_nc, varname='u', timestep='all')
    data_fromnc_v = get_ncmodeldata(file_nc=file_nc, varname='v', timestep='all')    
    vel_magn = np.sqrt(data_fromnc_u**2 + data_fromnc_v**2)

    fig, ax = plt.subplots()
    ax.plot(data_fromnc_edgex, data_fromnc_edgey,'-b',linewidth=0.2)
    ax.plot(data_fromnc_edgex.T, data_fromnc_edgey.T,'-b',linewidth=0.2)
    plt.savefig(os.path.join(dir_output,'SFINCS_meshedge'))    

    fig, axs = plt.subplots(3,1, figsize=(14,9))
    for iT, timestep in enumerate([0,1,10]):
        ax=axs[iT]
        pc = ax.pcolor(data_fromnc_edgex, data_fromnc_edgey,vel_magn[timestep,:,:],cmap='jet')
        pc.set_clim([0,0.6])
        cbar = fig.colorbar(pc, ax=ax)
        cbar.set_label('velocity magnitude (%s)'%(data_fromnc_u.var_ncvarobject.units))
        ax.set_title('t=%d (%s)'%(timestep, data_fromnc_u.var_times.loc[timestep]))
        ax.set_aspect('equal')
        thinning = 5
        ax.quiver(data_fromnc_edgex[::thinning,::thinning], data_fromnc_edgey[::thinning,::thinning], data_fromnc_u[timestep,::thinning,::thinning], data_fromnc_v[timestep,::thinning,::thinning], 
                  color='w')#,scale=3,width=0.005)#, edgecolor='face', cmap='jet')
    fig.tight_layout()
    plt.savefig(os.path.join(dir_output,'SFINCS_velocity_pcolorquiver'))


    #SFINCS HIS
    #file_nc = r'p:\11202255-sfincs\Testbed\Original_runs\01_Implementation\14_restartfile\sfincs_his.nc'
    file_nc = r'p:\11202255-sfincs\Testbed\Original_runs\03_Application\04_Tsunami_Japan_Sendai\sfincs_his.nc'
    vars_pd, dims_pd = get_ncvardimlist(file_nc=file_nc)
    
    station_names = get_hisstationlist(file_nc=file_nc, varname='point_zs')
    data_fromnc_his = get_ncmodeldata(file_nc=file_nc, varname='point_zs', station='all', timestep='all')

    fig, ax = plt.subplots()
    for iS,stat_name in enumerate(data_fromnc_his.var_stations['station_name']):
        ax.plot(data_fromnc_his.var_times, data_fromnc_his[:,iS], label=stat_name)
    ax.legend()
    plt.savefig(os.path.join(dir_output,'SFINCS_hiszs'))
    



    
@pytest.mark.acceptance
def test_exporttoshapefile():
    ## WARNING: THIS TEST IS NOT YET FINISHED, WILL BE IMPROVED AND LINKED TO INTERNAL FUNCTIONS ASAP
    dir_output = getmakeoutputdir(__file__,inspect.currentframe().f_code.co_name)
    """
    dir_output = './test_output'
    """

    import os
    import geopandas as gpd #conda install --channel conda-forge geopandas (breaks dfm_tools environment because of Qt issue)
    import pandas as pd
    from shapely.geometry import Point, Polygon
    import fiona
    from fiona.crs import from_epsg
    
    import numpy as np
    import matplotlib.pyplot as plt
    plt.close('all')
    
    from dfm_tools.get_nc import get_netdata, get_ncmodeldata, plot_netmapdata
    from dfm_tools.get_nc_helpers import get_ncvardimlist#, get_ncfilelist
    
    varlist = ['Chlfa']#,'mesh2d_s1']
    dir_shp = dir_output
    if not os.path.exists(dir_shp):
        os.makedirs(dir_shp)
    file_nc = os.path.join(r'p:\11203850-coastserv\06-Model\waq_model\simulations\run0_20200319\DFM_OUTPUT_kzn_waq', 'kzn_waq_0000_map.nc')
    
    vars_pd, dims_pd = get_ncvardimlist(file_nc=file_nc)
    vars_pd_matching = vars_pd[vars_pd.loc[:,'long_name'].str.match('.*Chl.*')]
    #vars_pd_matching = vars_pd[vars_pd.loc[:,'long_name'].str.startswith('') & vars_pd.loc[:,'long_name'].str.endswith('Chlo')]
    varns_Chl = vars_pd_matching['nc_varkeys'].tolist()
    varns_Chl_long = vars_pd_matching['long_name'].tolist()
    
    ugrid = get_netdata(file_nc=file_nc)#, multipart=False)
    
    pol_shp_list = []
    #partly from dfm_tools.ugrid.polygon_intersect()
    for iP, pol_data in enumerate(ugrid.verts): #[range(5000),:,:]
        pol_data_nonan = pol_data[~np.isnan(pol_data).all(axis=1)]
        pol_shp = Polygon(pol_data_nonan)
        pol_shp_list.append(pol_shp)
    
    print('creating geodataframe with cells')
    newdata = gpd.GeoDataFrame(crs="EPSG:4326")
    newdata['geometry'] = pol_shp_list #way more time efficient than doing it the loop
    
    for iV, varname in enumerate(varlist):
        newdata[varname] = None
    
    for timestep in [6]:#[0,10,20,30]:
        for iV, varname in enumerate(varlist):
            try:
                data_fromnc_all = get_ncmodeldata(file_nc=file_nc, varname=varname, timestep=timestep, layer='all')
                data_fromnc_bot = get_ncmodeldata(file_nc=file_nc, varname=varname, timestep=timestep, layer='bottom')
                data_fromnc_top = get_ncmodeldata(file_nc=file_nc, varname=varname, timestep=timestep, layer='top')
            except:
                data_fromnc_top = get_ncmodeldata(file_nc=file_nc, varname=varname, timestep=timestep)
    
            data_fromnc_nonan = data_fromnc_top[:]
            data_fromnc_nonan[data_fromnc_nonan.mask] = np.nan
            newdata[varname] = data_fromnc_nonan.data.flatten()
        file_shp = os.path.join(dir_shp,'shp_%s_%s'%(varname,data_fromnc_top.var_times.iloc[0].strftime('%Y%m%d')))
        newdata.to_file(file_shp)
        """
        fig, ax = plt.subplots(figsize=(6,7))
        pc = plot_netmapdata(ugrid.verts, values=data_fromnc_top.data.flatten(), ax=None, linewidth=0.5, cmap='jet')
        #pc.set_clim([-1,0])
        fig.colorbar(pc)
        ax.set_aspect(1./np.cos(np.mean(ax.get_ylim())/180*np.pi),adjustable='box')
        fig.tight_layout()
        """

import streamlit as st
import pandas as pd
import time
import pandas_ta as ta
from datetime import datetime, date, timedelta
import yfinance as yf

# Page configuration
st.set_page_config(
    page_title="Stock Analysis Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Stock Technical Analysis Dashboard")
st.markdown("---")

# Sidebar for inputs
st.sidebar.header("📊 Analysis Parameters")


start_d = st.sidebar.date_input(
    "Select Start Date",
    value=date(2008, 1, 1),
    min_value=date(1983, 1, 1),
    max_value=date(2030, 12, 31)
)

# Date input
manual_date = st.sidebar.date_input(
    "Select End Date",
    value=date(2025, 6, 1),
    min_value=date(1983, 1, 1),
    max_value=date(2030, 12, 31)
 )



ticker_list = [
    'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'BHARTIARTL.NS', 'ICICIBANK.NS', 'INFY.NS', 'SBIN.NS', 'LICI.NS', 'HINDUNILVR.NS', 'ITC.NS', 'LT.NS', 'HCLTECH.NS', 'BAJFINANCE.NS', 'SUNPHARMA.NS', 'NTPC.NS', 'MARUTI.NS', 'AXISBANK.NS', 'ONGC.NS', 'M&M.NS', 'KOTAKBANK.NS', 'TATAMOTORS.NS', 'ADANIENT.NS', 'ULTRACEMCO.NS', 'POWERGRID.NS', 'HAL.NS',
    'TITAN.NS', 'ADANIPORTS.NS', 'DMART.NS', 'COALINDIA.NS', 'WIPRO.NS', 'BAJAJ-AUTO.NS', 'ASIANPAINT.NS', 'BAJAJFINSV.NS', 'ADANIGREEN.NS', 'SIEMENS.NS', 'ADANIPOWER.NS', 'TRENT.NS', 'NESTLEIND.NS', 'JSWSTEEL.NS', 'ZOMATO.NS', 'HINDZINC.NS', 'IOC.NS', 'BEL.NS', 'IRFC.NS', 'JIOFIN.NS',
    'DLF.NS', 'VBL.NS', 'TATASTEEL.NS', 'VEDL.NS', 'LTIM.NS', 'GRASIM.NS', 'INDIGO.NS', 'SBILIFE.NS', 'PFC.NS', 'ABB.NS', 'TECHM.NS', 'PIDILITIND.NS', 'HINDALCO.NS', 'AMBUJACEM.NS', 'HYUNDAI.NS', 'HDFCLIFE.NS', 'RECLTD.NS', 'DIVISLAB.NS', 'GAIL.NS', 'BPCL.NS', 'TATAPOWER.NS', 'GODREJCP.NS',
    'BRITANNIA.NS', 'EICHERMOT.NS', 'MOTHERSON.NS', 'LODHA.NS', 'BANKBARODA.NS', 'CIPLA.NS', 'JSWENERGY.NS', 'TVSMOTOR.NS', 'PNB.NS', 'SHRIRAMFIN.NS', 'CHOLAFIN.NS', 'BAJAJHFL.NS', 'SWIGGY.NS', 'BAJAJHLDNG.NS', 'NTPCGREEN.NS', 'HAVELLS.NS', 'ADANIENSOL.NS', 'CGPOWER.NS', 'TORNTPHARM.NS',
    'DRREDDY.NS', 'IOB.NS', 'ZYDUSLIFE.NS', 'TATACONSUM.NS', 'UNITDSPR.NS', 'RVNL.NS', 'HEROMOTOCO.NS', 'DABUR.NS', 'ICICIPRULI.NS', 'BOSCHLTD.NS', 'POLYCAB.NS', 'INDUSTOWER.NS', 'CUMMINSIND.NS', 'NAUKRI.NS', 'INDHOTEL.NS', 'APOLLOHOSP.NS', 'MANKIND.NS', 'OFSS.NS', 'INDUSINDBK.NS',
    'ICICIGI.NS', 'JINDALSTEL.NS', 'SOLARINDS.NS', 'CANBK.NS', 'LUPIN.NS', 'MAXHEALTH.NS', 'SUZLON.NS', 'BHEL.NS', 'UNIONBANK.NS', 'SHREECEM.NS', 'IDBI.NS', 'NHPC.NS', 'HDFCAMC.NS', 'MAZDOCK.NS', 'OIL.NS', 'COLPAL.NS', 'ATGL.NS', 'DIXON.NS', 'MARICO.NS', 'PERSISTENT.NS',
    'HINDPETRO.NS', 'WAAREEENER.NS', 'GODREJPROP.NS', 'TORNTPOWER.NS', 'GMRAIRPORT.NS', 'AUROPHARMA.NS', 'IDEA.NS', 'POLICYBZR.NS', 'TIINDIA.NS', 'MUTHOOTFIN.NS', 'INDIANB.NS', 'PRESTIGE.NS', 'IRCTC.NS', 'SRF.NS', 'YESBANK.NS', 'GICRE.NS', 'BHARATFORG.NS', 'OBEROIRLTY.NS',
    'SBICARD.NS', 'ASHOKLEY.NS', 'ALKEM.NS', 'JSWINFRA.NS', 'KALYANKJIL.NS', 'NMDC.NS', 'BHARTIHEXA.NS', 'PIIND.NS', 'SUPREMEIND.NS', 'LINDEINDIA.NS', 'PATANJALI.NS', 'BERGEPAINT.NS', 'FACT.NS', 'PHOENIXLTD.NS', 'IREDA.NS', 'JSL.NS', 'UNOMINDA.NS', 'SCHAEFFLER.NS', 'UCOBANK.NS',
    'THERMAX.NS', 'BALKRISIND.NS', 'VOLTAS.NS', 'MRF.NS', 'MPHASIS.NS', 'CONCOR.NS', 'ABCAPITAL.NS', 'LTTS.NS', 'POWERINDIA.NS', 'SAIL.NS', 'TATACOMM.NS', 'NYKAA.NS', 'UBL.NS', 'PGHH.NS', 'ASTRAL.NS', 'IDFCFIRSTB.NS', 'PETRONET.NS', 'BANKINDIA.NS', 'HUDCO.NS', 'PREMIERENE.NS',
    'CENTRALBK.NS', 'BSE.NS', 'SUNDARMFIN.NS', 'COROMANDEL.NS', 'SJVN.NS', 'COCHINSHIP.NS', 'FEDERALBNK.NS', 'PAGEIND.NS', 'COFORGE.NS', 'AUBANK.NS', 'VMM.NS', 'MOTILALOFS.NS', 'LLOYDSME.NS', 'BDL.NS', 'KPITTECH.NS', 'TATAELXSI.NS', 'GVT&D.NS', 'GLENMARK.NS', 'GLAXO.NS',
    'ACC.NS', 'FORTIS.NS', 'PAYTM.NS', 'AWL.NS', 'NAM-INDIA.NS', 'HONAUT.NS', 'OLAELEC.NS', 'FLUOROCHEM.NS', 'MAHABANK.NS', 'BIOCON.NS', 'UPL.NS', 'ESCORTS.NS', 'JUBLFOOD.NS', 'APLAPOLLO.NS', 'EXIDEIND.NS', 'SONACOMS.NS', 'TATATECH.NS', 'LTF.NS', 'GUJGASLTD.NS', '360ONE.NS',
    '3MINDIA.NS', 'MFSL.NS', 'KEI.NS', 'AIAENG.NS', 'DEEPAKNTR.NS', 'NATIONALUM.NS', 'BLUESTARCO.NS', 'NIACL.NS', 'PSB.NS', 'APARINDS.NS', 'AJANTPHARM.NS', 'IPCALAB.NS', 'LICHSGFIN.NS', 'NLCINDIA.NS', 'M&MFIN.NS', 'IRB.NS', 'CRISIL.NS', 'GODREJIND.NS', 'DALBHARAT.NS',
    'SYNGENE.NS', 'ENDURANCE.NS', 'METROBRAND.NS', 'JKCEMENT.NS', 'KAYNES.NS', 'TATAINVEST.NS', 'IKS.NS', 'IGL.NS', 'ABFRL.NS', 'APOLLOTYRE.NS', 'FIRSTCRY.NS', 'STARHEALTH.NS', 'GODIGIT.NS', 'MRPL.NS', 'EMAMILTD.NS', 'KPRMILL.NS', 'CHOLAHLDNG.NS', 'SUNTV.NS', 'CDSL.NS',
    'MANYAVAR.NS', 'BANDHANBNK.NS', 'GLAND.NS', 'GODFRYPHLP.NS', 'MEDANTA.NS', 'MSUMI.NS', 'BRIGADE.NS', 'NBCC.NS', 'HINDCOPPER.NS', 'POONAWALLA.NS', 'PPLPHARMA.NS', 'SUVENPHAR.NS', 'JBCHEPHARM.NS', 'DELHIVERY.NS', 'GILLETTE.NS', 'CARBORUNIV.NS', 'ABREL.NS', 'BASF.NS',
    'ZFCVINDIA.NS', 'AEGISLOG.NS', 'ITI.NS', 'RADICO.NS', 'SUNDRMFAST.NS', 'TIMKEN.NS', 'TATACHEM.NS', 'CROMPTON.NS', 'ISEC.NS', 'JYOTICNC.NS', 'SUMICHEM.NS', 'LALPATHLAB.NS', 'INOXWIND.NS', 'HSCL.NS', 'LAURUSLABS.NS', 'EMCURE.NS', 'TVSHLTD.NS', 'GRINDWELL.NS', 'AIIL.NS',
    'WHIRLPOOL.NS', 'SKFINDIA.NS', 'ARE&M.NS', 'HATSUN.NS', 'NH.NS', 'NATCOPHARM.NS', 'KEC.NS', 'RATNAMANI.NS', 'PFIZER.NS', 'EIHOTEL.NS', 'CESC.NS', 'KIOCL.NS', 'PEL.NS', 'POLYMED.NS', 'ANGELONE.NS', 'PNBHOUSING.NS', 'IGIL.NS', 'CASTROLIND.NS', 'KANSAINER.NS', 'NUVAMA.NS',
    'IRCON.NS', 'JWL.NS', 'TRITURBINE.NS', 'SHYAMMETL.NS', 'ANANTRAJ.NS', 'FSL.NS', 'ATUL.NS', 'CAMS.NS', 'AFFLE.NS', 'TEJASNET.NS', 'FIVESTAR.NS', 'APLLTD.NS', 'ABSLAMC.NS', 'JBMA.NS', 'KAJARIACER.NS', 'DEVYANI.NS', 'GRSE.NS', 'CYIENT.NS', 'GSPL.NS', 'FINCABLES.NS',
    'ELGIEQUIP.NS', 'KIMS.NS', 'KPIL.NS', 'ASTERDM.NS', 'RAMCOCEM.NS', 'JINDALSAW.NS', 'BIKAJI.NS', 'AARTIIND.NS', 'CIEINDIA.NS', 'CHAMBLFERT.NS', 'VINATIORGA.NS', 'SIGNATURE.NS', 'SWANENERGY.NS', 'CONCORDBIO.NS', 'NCC.NS', 'VGUARD.NS', 'PTCIL.NS', 'SCHNEIDER.NS',
    'IIFL.NS', 'RELAXO.NS', 'HFCL.NS', 'BLUEDART.NS', 'CHALET.NS', 'CELLO.NS', 'AFCONS.NS', 'AADHARHFC.NS', 'WELCORP.NS', 'TBOTEK.NS', 'BATAINDIA.NS', 'RRKABEL.NS', 'TRIDENT.NS', 'SAGILITY.NS', 'JYOTHYLAB.NS', 'FINPIPE.NS', 'TITAGARH.NS', 'IDFC.NS', 'TECHNOE.NS',
    'SONATSOFTW.NS', 'CREDITACC.NS', 'KFINTECH.NS', 'GESHIP.NS', 'ERIS.NS', 'AMBER.NS', 'KARURVYSYA.NS', 'CENTURYPLY.NS', 'KIRLOSENG.NS', 'JAIBALAJI.NS', 'IFCI.NS', 'ASTRAZEN.NS', 'LMW.NS', 'BBTC.NS', 'BEML.NS', 'BSOFT.NS', 'RKFORGE.NS', 'DCMSHRIRAM.NS', 'NAVINFLUOR.NS',
    'WOCKPHARMA.NS', 'ASAHIINDIA.NS', 'CGCL.NS', 'ZENSARTECH.NS', 'IEX.NS', 'HBLENGINE.NS', 'NEWGEN.NS', 'VENTIVE.NS', 'APTUS.NS', 'SOBHA.NS', 'ANANDRATHI.NS', 'BLS.NS', 'JUBLPHARMA.NS', 'WELSPUNLIV.NS', 'TTML.NS', 'NEULANDLAB.NS', 'INDIAMART.NS', 'PCBL.NS', 'ACE.NS',
    'AKZOINDIA.NS', 'MANAPPURAM.NS', 'MGL.NS', 'KIRLOSBROS.NS', 'DOMS.NS', 'PGEL.NS', 'CLEAN.NS', 'FINEORG.NS', 'GRINFRA.NS', 'ZENTEC.NS', 'ACMESOLAR.NS', 'RITES.NS', 'REDINGTON.NS', 'SAILIFE.NS', 'KSB.NS', 'UTIAMC.NS', 'SANOFI.NS', 'SPLPETRO.NS', 'DATAPATTNS.NS',
    'NSLNISP.NS', 'INDGN.NS', 'GODREJAGRO.NS', 'PVRINOX.NS', 'RPOWER.NS', 'NIVABUPA.NS', 'NETWEB.NS', 'EIDPARRY.NS', 'CAPLIPOINT.NS', 'GRAVITA.NS', 'RAILTEL.NS', 'VTL.NS', 'ECLERX.NS', 'GRANULES.NS', 'SWSOLAR.NS', 'RAINBOW.NS', 'NAVA.NS', 'ELECON.NS', 'GPIL.NS',
    'SARDAEN.NS', 'PRAJIND.NS', 'AAVAS.NS', 'DEEPAKFERT.NS', 'INGERRAND.NS', 'RAYMONDLSL.NS', 'OLECTRA.NS', 'ZYDUSWELL.NS', 'HONASA.NS', 'MMTC.NS', 'CRAFTSMAN.NS', 'IWEL.NS', 'ZEEL.NS', 'WESTLIFE.NS', 'LTFOODS.NS', 'GLS.NS', 'JPPOWER.NS', 'MINDACORP.NS', 'CUB.NS',
    'INTELLECT.NS', 'NUVOCO.NS', 'RAYMOND.NS', 'CHENNPETRO.NS', 'AKUMS.NS', 'VOLTAMP.NS', 'TARIL.NS', 'TTKPRESTIG.NS', 'GENUSPOWER.NS', 'ALOKINDS.NS', 'RBLBANK.NS', 'ENGINERSIN.NS', 'RHIM.NS', 'MARKSANS.NS', 'HAPPSTMNDS.NS', 'TEGA.NS', 'AETHER.NS', 'JMFINANCIL.NS',
    'SAFARI.NS', 'CEATLTD.NS', 'SCI.NS', 'GMDCLTD.NS', 'J&KBANK.NS', 'MAHSCOOTER.NS', 'USHAMART.NS', 'TANLA.NS', 'STAR.NS', 'ELECTCAST.NS', 'SANOFICONR.NS', 'CANFINHOME.NS', 'BALRAMCHIN.NS', 'JUBLINGREA.NS', 'EUREKAFORB.NS', 'JSWHL.NS', 'MAPMYINDIA.NS', 'INDIACEM.NS',
    'KPIGREEN.NS', 'REDTAPE.NS', 'HAPPYFORGE.NS', 'METROPOLIS.NS', 'JKTYRE.NS', 'INOXINDIA.NS', 'CERA.NS', 'ALKYLAMINE.NS', 'VESUVIUS.NS', 'QUESS.NS', 'PRUDENT.NS', 'BAJAJELEC.NS', 'GRAPHITE.NS', 'PNCINFRA.NS', 'LEMONTREE.NS', 'SAPPHIRE.NS', 'NETWORK18.NS', 'ISGEC.NS',
    'GALAXYSURF.NS', 'RCF.NS', 'RTNINDIA.NS', 'SYMPHONY.NS', 'PURVA.NS', 'GPPL.NS', 'BIRLACORPN.NS', 'SAREGAMA.NS', 'DBREALTY.NS', 'BECTORFOOD.NS', 'ARVIND.NS', 'THOMASCOOK.NS', 'SFL.NS', 'RELINFRA.NS', 'LATENTVIEW.NS', 'EDELWEISS.NS', 'HOMEFIRST.NS', 'PNGJL.NS',
    'FORCEMOT.NS', 'JUSTDIAL.NS', 'ROUTE.NS', 'HGINFRA.NS', 'IONEXCHANG.NS', 'RENUKA.NS', 'VIJAYA.NS', 'SAMMAANCAP.NS', 'JKLAKSHMI.NS', 'AZAD.NS', 'ESABINDIA.NS', 'GNFC.NS', 'TIPSMUSIC.NS', 'WABAG.NS', 'TRIVENI.NS', 'KNRCON.NS', 'IIFLCAPS.NS', 'ABDL.NS', 'POWERMECH.NS',
    'CHOICEIN.NS', 'KIRLPNU.NS', 'AURIONPRO.NS', 'CCL.NS', 'SHAKTIPUMP.NS', 'SBFC.NS', 'PRSMJOHNSN.NS', 'JLHL.NS', 'TEXRAIL.NS', 'CAMPUS.NS', 'ITDCEM.NS', 'SHRIPISTON.NS', 'TIMETECHNO.NS', 'SENCO.NS', 'MASTEK.NS', 'LLOYDSENGG.NS', 'BBOX.NS', 'RATEGAIN.NS',
    'GSFC.NS', 'CMSINFO.NS', 'RUSTOMJEE.NS', 'MAXESTATES.NS', 'VARROC.NS', 'PGHL.NS', 'MAHSEAMLES.NS', 'HEG.NS', 'RELIGARE.NS', 'AVANTIFEED.NS', 'ACI.NS', 'EQUITASBNK.NS', 'SYRMA.NS', 'STARCEMENT.NS', 'BLUEJET.NS', 'ASKAUTOLTD.NS', 'GRWRHITECH.NS', 'SANSERA.NS',
    'FDC.NS', 'JUNIPER.NS', 'MEDPLUS.NS', 'GALLANTT.NS', 'KTKBANK.NS', 'MAHLIFE.NS', 'TCI.NS', 'TVSSCS.NS', 'GANESHHOUC.NS', 'ANURAS.NS', 'GMRP&UI.NS', 'SUNTECK.NS', 'EMBDL.NS', 'RTNPOWER.NS', 'MHRIL.NS', 'RAJESHEXPO.NS', 'GARFIBRES.NS', 'EPIGRAL.NS', 'JKPAPER.NS',
    'SHOPERSTOP.NS', 'INFIBEAM.NS', 'EPL.NS', 'MOIL.NS', 'ASTRAMICRO.NS', 'CHEMPLASTS.NS', 'SANDUMA.NS', 'AHLUCONT.NS', 'EMIL.NS', 'DIACABS.NS', 'TV18BRDCST.NS', 'UJJIVANSFB.NS', 'SHILPAMED.NS', 'INDIASHLTR.NS', 'PARADEEP.NS', 'ETHOSLTD.NS', 'ICIL.NS', 'VMART.NS',
    'LXCHEM.NS', 'WELENT.NS', 'HCC.NS', 'DBL.NS', 'MIDHANI.NS', 'PDSL.NS', 'MANINFRA.NS', 'IFBIND.NS', 'TRANSRAILL.NS', 'DHANUKA.NS', 'TMB.NS', 'ORCHPHARMA.NS', 'NAZARA.NS', 'RESPONIND.NS', 'EMUDHRA.NS', 'ARVINDFASN.NS', 'DODLA.NS', 'SUNDARMHLD.NS', 'BALUFORGE.NS',
    'TIIL.NS', 'INDIGOPNTS.NS', 'SUPRAJIT.NS', 'BALAMINES.NS', 'GREENLAM.NS', 'SPARC.NS', 'JINDWORLD.NS', 'SUDARSCHEM.NS', 'UNIMECH.NS', 'GABRIEL.NS', 'ASHOKA.NS', 'VIPIND.NS', 'SURYAROSNI.NS', 'BLACKBUCK.NS', 'KRBL.NS', 'GOKEX.NS', 'SHARDAMOTR.NS', 'AMIORG.NS',
    'NESCO.NS', 'KESORAMIND.NS', 'HNDFDS.NS', 'ORIENTCEM.NS', 'SOUTHBANK.NS', 'TARC.NS', 'BORORENEW.NS', 'TDPOWERSYS.NS', 'EASEMYTRIP.NS', 'NIITMTS.NS', 'BANSALWIRE.NS', 'RALLIS.NS', 'PRIVISCL.NS', 'CEIGALL.NS', 'JAICORPLTD.NS', 'VSTIND.NS', 'NFL.NS', 'STLTECH.NS',
    'ICRA.NS', 'PILANIINVS.NS', 'ROLEXRINGS.NS', 'AVL.NS', 'GOCOLORS.NS', 'UEL.NS', 'GULFOILLUB.NS', 'LUXIND.NS', 'PCJEWELLER.NS', 'GMMPFAUDLR.NS', 'GAEL.NS', 'SHAREINDIA.NS', 'IXIGO.NS', 'AGI.NS', 'LLOYDSENT.NS', 'PRINCEPIPE.NS', 'PRICOLLTD.NS', 'GHCL.NS',
    'ALLCARGO.NS', 'JKIL.NS', 'ITDC.NS', 'TI.NS', 'HCG.NS', 'DBCORP.NS', 'SIS.NS', 'GUJALKALI.NS', 'RSYSTEMS.NS', 'PTC.NS', 'ENTERO.NS', 'SHARDACROP.NS', 'INOXGREEN.NS', 'AARTIPHARM.NS', 'RAIN.NS', 'CSBBANK.NS', 'CYIENTDLM.NS', 'THANGAMAYL.NS', 'BANCOINDIA.NS',
    'JSFB.NS', 'JCHAC.NS', 'HEMIPROP.NS', 'MTARTECH.NS', 'NPST.NS', 'ORIENTELEC.NS', 'MANORAMA.NS', 'MSTCLTD.NS', 'PAISALO.NS', 'KIRLOSIND.NS', 'OPTIEMUS.NS', 'ANUP.NS', 'EIEL.NS', 'BBL.NS', 'DYNAMATECH.NS', 'MASFIN.NS', 'HEIDELBERG.NS', 'ZAGGLE.NS', 'HERITGFOOD.NS',
    'VAIBHAVGBL.NS', 'KSCL.NS', 'TEAMLEASE.NS', 'CARTRADE.NS', 'RBA.NS', 'NEOGEN.NS', 'SKIPPER.NS', 'GANECOS.NS', 'VRLLOG.NS', 'AWFIS.NS', 'BOROLTD.NS', 'GOPAL.NS', 'UTKARSHBNK.NS', 'REFEX.NS', 'E2E.NS', 'WONDERLA.NS', 'ADVENZYMES.NS', 'BHARATRAS.NS', 'SHAILY.NS',
    'BAJAJHIND.NS', 'UNICHEMLAB.NS', 'ORISSAMINE.NS', 'PATELENG.NS', 'YATHARTH.NS', 'HARSHA.NS', 'NOCIL.NS', 'GATEWAY.NS', 'ROSSARI.NS', 'JAMNAAUTO.NS', 'SUPRIYA.NS', 'AARTIDRUGS.NS', 'WEBELSOLAR.NS', 'JISLJALEQS.NS', 'THYROCARE.NS', 'PITTIENG.NS', 'PGIL.NS',
    'RAMKY.NS', 'JTEKTINDIA.NS', 'STYRENIX.NS', 'HIKAL.NS', 'UFLEX.NS', 'PARAS.NS', 'GREENPANEL.NS', 'SHANTIGEAR.NS', 'SUBROS.NS', 'BOMDYEING.NS', 'EMSLIMITED.NS', 'INNOVACAP.NS', 'MOBIKWIK.NS', 'SUNCLAY.NS', 'JAYNECOIND.NS', 'GREENPLY.NS', 'BALMLAWRIE.NS', 'IMAGICAA.NS',
    'SEQUENT.NS', 'ORIANA.NS', 'BANARISUG.NS', 'SAMHI.NS', 'FEDFINA.NS', 'BHAGCHEM.NS', 'EXICOM.NS', 'GREAVESCOT.NS', 'AVALON.NS', 'LGBBROSLTD.NS', 'MEDIASSIST.NS', 'AVANTEL.NS', 'SKYGOLD.NS', 'PFOCUS.NS', 'ISMTLTD.NS', 'SUNFLAG.NS', 'FCL.NS', 'MOREPENLAB.NS',
    'NORTHARC.NS', 'VENUSPIPES.NS', 'V2RETAIL.NS', 'GUFICBIO.NS', 'JTLIND.NS', 'FIEMIND.NS', 'CIGNITITEC.NS', 'WSTCSTPAPR.NS', 'IMFA.NS', 'TCIEXP.NS', 'KKCL.NS', 'KPEL.NS', 'JSLL.NS', 'GOKULAGRO.NS', 'KRN.NS', 'SOTL.NS', 'SULA.NS', 'JNKINDIA.NS', 'DCBBANK.NS',
    'DCXINDIA.NS', 'VSTTILLERS.NS', 'INDIAGLYCO.NS', 'KSL.NS', 'DHANI.NS', 'KDDL.NS', 'SPANDANA.NS', 'VEEDOL.NS', 'SEPC.NS', 'ARTEMISMED.NS', 'LUMAXTECH.NS', 'POLYPLEX.NS', 'SWARAJENG.NS', 'HONDAPOWER.NS', 'KINGFA.NS', 'LAOPALA.NS', 'ARVSMART.NS', 'PARKHOTELS.NS',
    'MUTHOOTMF.NS', 'HGS.NS', 'STYLAMIND.NS', 'HMT.NS', 'MPSLTD.NS', 'INDRAMEDCO.NS', 'RPGLIFE.NS', 'SANGHVIMOV.NS', 'CARRARO.NS', 'BEPL.NS', 'JINDALPOLY.NS', 'DATAMATICS.NS', 'HPL.NS', 'DALMIASUG.NS', 'ALEMBICLTD.NS', 'SCILAL.NS', 'HATHWAY.NS', 'TCNSBRANDS.NS',
    'CARERATING.NS', 'SHK.NS', 'SBCL.NS', 'MTNL.NS', 'SEAMECLTD.NS', 'INDOSTAR.NS', 'SERVOTECH.NS', 'ASHIANA.NS', 'SANDHAR.NS', 'GIPCL.NS', 'DPABHUSHAN.NS', 'EPACK.NS', 'SINDHUTRAD.NS', 'BAJAJCON.NS', 'SSWL.NS', 'QUICKHEAL.NS', 'NUCLEUS.NS', 'DELTACORP.NS',
    'NAVNETEDUL.NS', 'TIRUMALCHM.NS', 'BFUTILITIE.NS', 'MAHLOG.NS', 'RPSGVENT.NS', 'GENSOL.NS', 'GOLDIAM.NS', 'VPRPL.NS', 'MARINE.NS', 'PRAKASH.NS', 'GEOJITFSL.NS', 'GOODLUCK.NS', 'MAITHANALL.NS', 'KITEX.NS', 'SJS.NS', 'PRECWIRE.NS', 'GTLINFRA.NS', 'DCAL.NS',
    'FLAIR.NS', 'SANATHAN.NS', 'TVSSRICHAK.NS', 'PFS.NS', 'SAKSOFT.NS', 'APOLLO.NS', 'CAPACITE.NS', 'REPCOHOME.NS', 'MARATHON.NS', 'INDOCO.NS', 'BAJEL.NS', 'KCP.NS', 'SURAJEST.NS', 'ASHAPURMIN.NS', 'WENDT.NS', 'GENESYS.NS', 'JASH.NS', 'POKARNA.NS', 'ADFFOODS.NS',
    'EVEREADY.NS', 'SALASAR.NS', 'FINOPB.NS', 'SAGCEM.NS', 'NSIL.NS', 'TASTYBITE.NS', 'RPEL.NS', 'HINDOILEXP.NS', 'SUVEN.NS', 'KOLTEPATIL.NS', 'PREMEXPLN.NS', 'SPECTRUM.NS', 'NRBBEARING.NS', 'DOLLAR.NS', 'ORIENTHOT.NS', 'SOMANYCERA.NS', 'IDEAFORGE.NS', 'FOSECOIND.NS',
    'VADILALIND.NS', 'AJMERA.NS', 'HITECH.NS', 'AUTOAXLES.NS', 'GLOBUSSPR.NS', 'GEPIL.NS', 'TCPLPACK.NS', 'NILKAMAL.NS', 'ARKADE.NS', 'SUMMITSEC.NS', 'RAJRATAN.NS', 'DREDGECORP.NS', 'STANLEY.NS', 'VISHNU.NS', 'FUSION.NS', 'THEJO.NS', 'SHALBY.NS', 'DEEPINDS.NS',
    'VENKEYS.NS', 'HLEGLAS.NS', 'KICL.NS', 'DAMCAPITAL.NS', 'VINDHYATEL.NS', 'FILATEX.NS', 'SIYSIL.NS', 'MONARCH.NS', 'MAYURUNIQ.NS', 'MMFL.NS', 'UNITECH.NS', 'HUHTAMAKI.NS', 'RANEHOLDIN.NS', 'SMLISUZU.NS', 'VAKRANGEE.NS', 'SASKEN.NS', 'KALAMANDIR.NS', 'RPTECH.NS',
    'HINDWAREAP.NS', 'PSPPROJECT.NS', 'KRSNAA.NS', 'CONFIPET.NS', 'XPROINDIA.NS', 'LANDMARK.NS', 'SENORES.NS', 'STYLEBAAZA.NS', 'STOVEKRAFT.NS', 'SOLARA.NS', 'DCW.NS', 'SABTNL.NS', 'JYOTISTRUC.NS', 'ACCELYA.NS', 'EIHAHOTELS.NS', 'PENIND.NS', 'SMSPHARMA.NS',
    'DOLATALGO.NS', 'DISHTV.NS', 'MANGLMCEM.NS', 'BFINVEST.NS', 'PRECAM.NS', 'IOLCP.NS', 'INTERARCH.NS', 'MOLDTKPAC.NS', 'RAMRAT.NS', 'JUBLINDS.NS', 'LUMAXIND.NS', 'INDIANHUME.NS', 'MANINDS.NS', 'UDS.NS', 'INSECTICID.NS', 'MOL.NS', 'THEMISMED.NS', 'DREAMFOLKS.NS',
    'PIXTRANS.NS', 'ECOSMOBLTY.NS', 'PARACABLES.NS', 'ESAFSFB.NS', 'DOLPHIN.NS', 'INDOTECH.NS', 'TARSONS.NS', 'DEN.NS', 'KMEW.NS', 'HMAAGRO.NS', 'PANAMAPET.NS', 'NELCO.NS', 'AEROFLEX.NS', 'MOTISONS.NS', 'PARAGMILK.NS', 'FMGOETZE.NS', 'VIDHIING.NS', 'IPL.NS',
    'OWAIS.NS', 'NITINSPIN.NS', 'APOLLOPIPE.NS', '63MOONS.NS', 'DIAMONDYD.NS', 'AXISCADES.NS', 'UGROCAP.NS', 'SANSTAR.NS', 'ASTEC.NS', 'RUPA.NS', 'CUPID.NS', 'UNIVCABLES.NS', 'TATVA.NS', 'SPAL.NS', 'CENTUM.NS', 'CARYSIL.NS', 'BARBEQUE.NS', 'VSSL.NS', 'GREENPOWER.NS',
    'RAMCOIND.NS', 'TIL.NS', 'MUKANDLTD.NS', 'JITFINFRA.NS', 'SANGHIIND.NS', 'NIITLTD.NS', 'TTKHLTCARE.NS', 'AHL.NS', 'IKIO.NS', 'POCL.NS', 'OMAXE.NS', 'PNBGILTS.NS', 'KIRIINDUS.NS', 'DEEDEV.NS', 'AMRUTANJAN.NS', 'KODYTECH.NS', 'YASHO.NS', 'ATFL.NS', 'COSMOFIRST.NS',
    'APCOTEXIND.NS', 'SDBL.NS', 'HESTERBIO.NS', 'GANDHAR.NS', 'IGARASHI.NS', 'ALPEXSOLAR.NS', 'HUBTOWN.NS', 'PLATIND.NS', 'ANDHRAPAP.NS', 'CANTABIL.NS', 'GOCLCORP.NS', 'SURAKSHA.NS', 'UNIPARTS.NS', 'SBGLP.NS', 'NAVKARCORP.NS', 'HIL.NS', 'SESHAPAPER.NS', 'BLKASHYAP.NS',
    'DLINKINDIA.NS', 'SATIN.NS', 'IFGLEXPOR.NS', 'EKC.NS', 'ALICON.NS', 'SANGAMIND.NS', 'TAJGVK.NS', 'TALBROAUTO.NS', 'UNIECOM.NS', 'MICEL.NS', 'EXPLEOSOL.NS', 'BLSE.NS', 'VERANDA.NS', 'AWHCL.NS', 'JAGRAN.NS', 'DIVGIITTS.NS', 'JINDRILL.NS', 'HARIOMPIPE.NS', 'MBAPL.NS',
    'YATRA.NS', 'SHRIRAMPPS.NS', 'VERTOZ.NS', 'MASTERTR.NS', 'WINDLAS.NS', 'JPASSOCIAT.NS', 'GMBREW.NS', 'UDAICEMENT.NS', 'WEL.NS', 'STERTOOLS.NS', 'WHEELS.NS', 'RAMASTEEL.NS', 'ROSSTECH.NS', 'BSHSL.NS', 'RELTD.NS', 'GPTINFRA.NS', 'SIRCA.NS', 'GKWLIMITED.NS',
    'CAMLINFINE.NS', 'IGPL.NS', 'DANISH.NS', 'SALZERELEC.NS', 'GRPLTD.NS', 'ROTO.NS', 'SYNCOMF.NS', 'SIGACHI.NS', 'DPSCLTD.NS', 'MUFIN.NS', 'HERANBA.NS', 'EXCELINDUS.NS', 'GNA.NS', 'SUYOG.NS', 'SURYODAY.NS', 'RIIL.NS', 'ATULAUTO.NS', 'GTPL.NS', 'SADHNANIQ.NS',
    'ADORWELD.NS', 'PANACEABIO.NS', 'SAHASRA.NS', 'AGARIND.NS', 'DSSL.NS', 'GODAVARIB.NS', 'BIGBLOC.NS', 'HIRECT.NS', 'SWELECTES.NS', 'DCMSRIND.NS', 'BCG.NS', 'WALCHANNAG.NS', 'IRMENERGY.NS', 'BHARATWIRE.NS', 'PENINLAND.NS', 'INDNIPPON.NS', 'KOKUYOCMLN.NS',
    'ARMANFIN.NS', 'MADRASFERT.NS', 'ZOTA.NS', 'BOROSCI.NS', 'SPIC.NS', 'OAL.NS', 'NDRAUTO.NS', 'HIMATSEIDE.NS', 'HITECHGEAR.NS', 'OMINFRAL.NS', 'BETA.NS', 'TEXINFRA.NS', 'AMNPLST.NS', 'MANGCHEFER.NS', 'DYCL.NS', 'BCLIND.NS', 'RML.NS', 'MSPL.NS', 'ASALCBR.NS',
    'EVERESTIND.NS', 'CEWATER.NS', 'MONTECARLO.NS', 'TFCILTD.NS', 'ALLDIGI.NS', 'BUTTERFLY.NS', 'EIMCOELECO.NS', 'SMCGLOBAL.NS', '5PAISA.NS', 'MATRIMONY.NS', 'YUKEN.NS', 'IMPAL.NS', 'LIKHITHA.NS', 'KABRAEXTRU.NS', 'SUBEXLTD.NS', 'FAIRCHEMOR.NS', 'SPORTKING.NS',
    'TECHLABS.NS', 'TBZ.NS', 'STEELCAS.NS', 'WINDMACHIN.NS', 'CENTRUM.NS', 'VINCOFE.NS', 'ARIHANTSUP.NS', 'DVL.NS', 'CLSEL.NS', 'HEXATRADEX.NS', 'TNPL.NS', 'RICOAUTO.NS', 'MAMATA.NS', 'RAMCOSYS.NS', 'SHANKARA.NS', 'ORIENTTECH.NS', 'PVSL.NS', 'PUNJABCHEM.NS',
    'ASIANENE.NS', 'GPTHEALTH.NS', 'ANDHRSUGAR.NS', 'SOLEX.NS', 'KRISHANA.NS', 'AGIIL.NS', 'KELLTONTEC.NS', 'JGCHEM.NS', 'RISHABH.NS', 'ACLGATI.NS', 'CENTENKA.NS', 'VIMTALABS.NS', 'KAMDHENU.NS', 'VASCONEQ.NS', 'BESTAGRO.NS', 'REMUS.NS', 'ADSL.NS', 'SHREDIGCEM.NS',
    'KERNEX.NS', 'LINCOLN.NS', 'SPCENET.NS', 'WEALTH.NS', 'SIGNPOST.NS', 'ONEPOINT.NS', 'VLEGOV.NS', 'MACPOWER.NS', 'HERCULES.NS', 'VHL.NS', 'TVTODAY.NS', 'MANALIPETC.NS', 'CAPITALSFB.NS', 'BLISSGVS.NS', 'ESTER.NS', 'WCIL.NS', 'CHEMFAB.NS', 'GRMOVER.NS',
    'SAURASHCEM.NS', 'RGL.NS', 'KROSS.NS', 'SPMLINFRA.NS', 'DHAMPURSUG.NS', 'NGLFINE.NS', 'XCHANGING.NS', 'KECL.NS', 'CREST.NS', 'KOPRAN.NS', 'SELAN.NS', 'MUKKA.NS', 'AVADHSUGAR.NS', 'HLVLTD.NS', 'SATINDLTD.NS', 'AVTNPL.NS', 'RAJRILTD.NS', 'PPL.NS', 'VLSFINANCE.NS',
    'DWARKESH.NS', 'SNOWMAN.NS', 'RKSWAMY.NS', 'PDMJEPAPER.NS', 'GULPOLY.NS', 'JAGSNPHARM.NS', 'INDOAMIN.NS', 'SANDESH.NS', 'ASAL.NS', 'CONTROLPR.NS', 'SAHANA.NS', 'ELECTHERM.NS', 'SIMPLEXINF.NS', 'OSWALGREEN.NS', 'STEELXIND.NS', 'KUANTUM.NS', 'GICHSGFIN.NS',
    'GALAPREC.NS', 'UTTAMSUGAR.NS', 'ICEMAKE.NS', 'HEUBACHIND.NS', 'RADHIKAJWE.NS', 'NDTV.NS', 'DIFFNKG.NS', 'KSOLVES.NS', 'ARROWGREEN.NS', 'MVGJL.NS', 'MUFTI.NS', 'DHUNINV.NS', 'MAXIND.NS', 'PAKKA.NS', 'ROSSELLIND.NS', 'CREATIVE.NS', 'KOTHARIPET.NS', 'APTECHT.NS',
    'INDORAMA.NS', 'HARDWYN.NS', 'NACLIND.NS', 'C2C.NS', 'SRHHYPOLTD.NS', 'NELCAST.NS', 'UNIENTER.NS', 'SATIA.NS', 'VILAS.NS', 'VINYAS.NS', 'MUNJALAU.NS', 'FAZE3Q.NS', 'ANUHPHR.NS', 'BAJAJHCARE.NS', 'ATL.NS', 'MAGADSUGAR.NS', 'BLAL.NS', 'ELIN.NS', 'GGBL.NS',
    'SHALPAINTS.NS', 'JAYBARMARU.NS', 'GANESHBE.NS', 'DHARMAJ.NS', 'AGSTRA.NS', 'BASILIC.NS', 'SUTLEJTEX.NS', 'TREL.NS', 'NAHARSPING.NS', 'VALIANTORG.NS', 'ZEEMEDIA.NS', 'ZUARIIND.NS', 'SARTELE.NS', 'INFOBEAN.NS', 'AIMTRON.NS', 'URJA.NS', 'STCINDIA.NS', 'KRYSTAL.NS',
    'GANDHITUBE.NS', 'CELLECOR.NS', 'SSEGL.NS', 'THEINVEST.NS', 'KAMOPAINTS.NS', 'SASTASUNDR.NS', 'DENTALKART.NS', 'KRITI.NS', 'KRISHNADEF.NS', 'ARIHANTCAP.NS', 'NINSYS.NS', 'EMKAYTOOLS.NS', 'AYMSYNTEX.NS', 'NCLIND.NS', 'ENIL.NS', 'APS.NS', 'RSWM.NS',
    'ASIANTILES.NS', 'ORIENTPPR.NS', 'KOTYARK.NS', 'BODALCHEM.NS', 'DHANBANK.NS', 'BIRLAMONEY.NS', 'INNOVANA.NS', 'GVKPIL.NS', 'GHCLTEXTIL.NS', 'SICALLOG.NS', 'RATNAVEER.NS', 'SHIVALIK.NS', 'AMBIKCO.NS', 'GFLLIMITED.NS', 'ROHLTD.NS', 'LINC.NS', 'PRIMESECU.NS',
    '20MICRONS.NS', 'RUSHIL.NS', 'SBC.NS', 'RACLGEAR.NS', 'RITCO.NS', 'MINDTECK.NS', 'CHEMCON.NS', 'ESFL.NS', 'SARVESHWAR.NS', 'FILATFASH.NS', 'ZODIAC.NS', 'SILVERTUC.NS', 'GIRIRAJ.NS', 'CSLFINANCE.NS', 'ESSARSHPNG.NS', 'MALLCOM.NS', 'TRACXN.NS', 'VHLTD.NS',
    'STEL.NS', 'GARUDA.NS', 'VISAKAIND.NS', 'JAYAGROGN.NS', 'OSWALAGRO.NS', 'UGARSUGAR.NS', 'ALLETEC.NS', 'ELDEHSG.NS', 'JPOLYINVST.NS', 'ZUARI.NS', 'DBL.NS', 'BHAGERIA.NS', 'DECCANCE.NS', 'MMP.NS', 'ONWARDTEC.NS', 'RUBYMILLS.NS', 'FOODSIN.NS', 'SJLOGISTIC.NS',
    'JINDALPHOT.NS', 'CAREERP.NS', 'RADIANTCMS.NS', 'ONMOBILE.NS', 'REPRO.NS', 'COFFEEDAY.NS', 'SHREEPUSHK.NS', 'GEECEE.NS', 'VMARCIND.NS', 'GSLSU.NS', 'SAKUMA.NS', 'HPAL.NS', 'SUKHJITS.NS', 'TIRUPATI.NS', 'MAANALU.NS', 'GLOSTERLTD.NS', 'LIBERTSHOE.NS', 'SPENCERS.NS',
    'NECLIFE.NS', 'ACL.NS', 'TPLPLASTEH.NS', 'SARLAPOLY.NS', 'WSI.NS', 'FOCUS.NS', 'TNPETRO.NS', 'CHEVIOT.NS', 'TRANSWORLD.NS', 'CHEMBOND.NS', 'RBL.NS', 'KDL.NS', 'HINDCOMPOS.NS', 'SPECIALITY.NS', 'DENORA.NS', 'DBEIL.NS', 'SURAJLTD.NS', 'DIGISPICE.NS', 'APEX.NS',
    'ALBERTDAVD.NS', 'SCHAND.NS', 'TAC.NS', 'TOLINS.NS', 'MANBA.NS', 'NDL.NS', 'PARSVNATH.NS', 'WANBURY.NS', 'VRAJ.NS', 'VIKASLIFE.NS', 'CCCL.NS', 'BIL.NS', 'PASHUPATI.NS', 'INDSWFTLAB.NS', 'DMCC.NS', 'KHAICHEM.NS', 'PVP.NS', 'ANNAPURNA.NS', 'JAYBEE.NS',
    'AFFORDABLE.NS', 'PLASTIBLEN.NS', 'BIRLACABLE.NS', 'RPPINFRA.NS', 'RBMINFRA.NS', 'EMAMIPAP.NS', 'INDOTHAI.NS', 'VISHNUINFR.NS', 'RVTH.NS', 'NRL.NS', 'FOCE.NS', 'TVSELECT.NS', 'MENONBE.NS', 'NITCO.NS', 'VINYLINDIA.NS', 'PYRAMID.NS', 'LOKESHMACH.NS', 'ASHIMASYN.NS',
    'BALAJITELE.NS', 'BEDMUTHA.NS', 'HMVL.NS', 'SAKAR.NS', 'LGHL.NS', 'GOACARBON.NS', 'KHADIM.NS', 'DEEPENR.NS', 'CONSOFINVT.NS', 'MBLINFRA.NS', 'NAHARPOLY.NS', 'RBZJEWEL.NS', 'NRAIL.NS', 'MEGATHERM.NS', 'KRITINUT.NS', 'COOLCAPS.NS', 'DONEAR.NS', 'GANESHIN.NS',
    'RSSOFTWARE.NS', 'ADVANIHOTR.NS', 'SKMEGGPROD.NS', 'SILINV.NS', 'ABSMARINE.NS', 'CYBERTECH.NS', 'TCLCONS.NS', 'IRIS.NS', 'KNAGRI.NS', 'MOLDTECH.NS', 'RACE.NS', 'MOS.NS', 'PCCL.NS', 'DAVANGERE.NS', 'SUPREMEPWR.NS', 'BCONCEPTS.NS', 'ALANKIT.NS', 'SREEL.NS',
    'IITL.NS', 'INDOUS.NS', 'KANORICHEM.NS', 'PREMIERPOL.NS', 'LAWSIKHO.NS', 'SHIVAMAUTO.NS', 'VINSYS.NS', 'INTLCONV.NS', 'IRISDOREME.NS', 'MODISONLTD.NS', 'BALAXI.NS', '3IINFOLTD.NS', 'NAHARCAP.NS', 'MAZDA.NS', 'ZIMLAB.NS', 'KILITCH.NS', 'GEEKAYWIRE.NS',
    'DIAMINESQ.NS', 'SINCLAIR.NS', 'AXITA.NS', 'URAVI.NS', 'ASAHISONG.NS', 'MIRCELECTR.NS', 'TRF.NS', 'IFBAGRO.NS', 'UYFINCORP.NS', 'PROV.NS', 'APCL.NS', 'SADBHAV.NS', 'SRD.NS', 'VALIANTLAB.NS', 'VIVIANA.NS', 'TEMBO.NS', 'ORIENTBELL.NS', 'MANAKCOAT.NS',
    'FROG.NS', 'NILAINFRA.NS', 'INSPIRISYS.NS', 'GOKUL.NS', 'UTSSAV.NS', 'BANSWRAS.NS', 'ALMONDZ.NS', 'ELGIRUBCO.NS', 'UNIDT.NS', 'KOTHARIPRO.NS', 'RADIOCITY.NS', 'ORBTEXP.NS', 'MEGASOFT.NS', 'SHREEKARNI.NS'
  ]






# Add option to customize ticker list
st.sidebar.subheader("📋 Stock Symbols")
custom_tickers = st.sidebar.text_area(
    "Add/Edit Tickers (one per line)",
    value="\n".join(ticker_list),
    height=120    
)

ticker_list = [ticker.strip() for ticker in custom_tickers.split('\n') if ticker.strip()]



# Function definitions
@st.cache_data
def create_trading_calendar():
    """Create trading calendar with NSE holidays"""
    current_year = 2025
    last_year = current_year - 1
    start_date_cal = date(last_year, 1, 1)
    end_date_cal = date(current_year, 12, 31)
    
    calendar_df = pd.DataFrame(index=pd.date_range(start=start_date_cal, end=end_date_cal, freq='D'))
    calendar_df['Date'] = calendar_df.index
    calendar_df['Day'] = calendar_df.index.strftime('%A')
    calendar_df['Year'] = calendar_df.index.year
    calendar_df['Trading Day'] = ~calendar_df['Day'].isin(['Saturday', 'Sunday'])
    
    # NSE Holidays for 2024-2025
    holidays = [
    '2007-01-26','2007-03-02','2007-04-06','2007-04-14','2007-05-01','2007-08-15','2007-08-24','2007-10-02','2007-11-09','2007-12-25',
    '2008-01-26','2008-03-06','2008-03-21','2008-04-14','2008-05-01','2008-08-15','2008-09-03','2008-10-02','2008-10-28','2008-12-25',
    '2009-01-26','2009-03-11','2009-04-10','2009-04-14','2009-05-01','2009-08-15','2009-08-23','2009-10-02','2009-10-17','2009-12-25',
    '2010-01-26','2010-03-01','2010-04-02','2010-04-14','2010-05-01','2010-08-15','2010-09-11','2010-10-02','2010-11-05','2010-12-25',
    '2011-01-26','2011-03-19','2011-04-22','2011-04-14','2011-05-01','2011-08-15','2011-09-01','2011-10-02','2011-10-26','2011-12-25',
    '2012-01-26','2012-03-08','2012-04-06','2012-04-14','2012-05-01','2012-08-15','2012-09-19','2012-10-02','2012-11-13','2012-12-25',
    '2013-01-26','2013-03-27','2013-03-29','2013-04-14','2013-05-01','2013-08-15','2013-09-09','2013-10-02','2013-11-03','2013-12-25',
    '2014-01-26','2014-03-17','2014-04-18','2014-04-14','2014-05-01','2014-08-15','2014-08-29','2014-10-02','2014-10-23','2014-12-25',
    '2015-01-26','2015-03-06','2015-04-03','2015-04-14','2015-05-01','2015-08-15','2015-09-17','2015-10-02','2015-11-11','2015-12-25',
    '2016-01-26','2016-03-24','2016-03-25','2016-04-14','2016-05-01','2016-08-15','2016-09-05','2016-10-02','2016-10-30','2016-12-25',
    '2017-01-26','2017-03-13','2017-04-14','2017-04-14','2017-05-01','2017-08-15','2017-08-25','2017-10-02','2017-10-19','2017-12-25',
    '2018-01-26','2018-03-02','2018-03-30','2018-04-14','2018-05-01','2018-08-15','2018-09-13','2018-10-02','2018-11-07','2018-12-25',
    '2019-01-26','2019-03-21','2019-04-19','2019-04-14','2019-05-01','2019-08-15','2019-09-02','2019-10-02','2019-10-27','2019-12-25',
    '2020-01-26','2020-03-10','2020-04-10','2020-04-14','2020-05-01','2020-08-15','2020-08-22','2020-10-02','2020-11-14','2020-12-25',
    '2021-01-26','2021-03-29','2021-04-02','2021-04-14','2021-05-01','2021-08-15','2021-09-10','2021-10-02','2021-11-04','2021-12-25',
    '2022-01-26','2022-03-18','2022-04-15','2022-04-14','2022-05-01','2022-08-15','2022-08-31','2022-10-02','2022-10-24','2022-12-25',
    '2023-01-26','2023-03-08','2023-04-07','2023-04-14','2023-05-01','2023-08-15','2023-09-19','2023-10-02','2023-11-12','2023-12-25',
    '2024-01-26','2024-03-08','2024-03-25','2024-03-29','2024-04-11','2024-04-14','2024-04-17','2024-05-01','2024-06-17','2024-08-15','2024-09-07','2024-10-02','2024-10-31','2024-11-01','2024-11-15','2024-12-25',
    '2025-01-26','2025-02-26','2025-03-14','2025-03-31','2025-04-06','2025-04-10','2025-04-14','2025-04-18','2025-05-01','2025-06-07','2025-07-06','2025-08-15','2025-08-27','2025-10-02','2025-10-21','2025-10-22','2025-11-05','2025-12-25'
     ]

    holiday_dates = pd.to_datetime(holidays)
    calendar_df.loc[calendar_df.index.isin(holiday_dates), 'Trading Day'] = False
    
    return calendar_df[calendar_df['Trading Day'] == True]

@st.cache_data
def create_historical_calendar():
    """Create historical trading calendar from 2008-2025"""
    hist_start = date(2008, 1, 1)
    hist_end = date(2025, 12, 31)
    historical_calendar = pd.DataFrame(index=pd.date_range(start=hist_start, end=hist_end, freq='D'))
    historical_calendar['Day'] = historical_calendar.index.strftime('%A')
    historical_calendar['Trading Day'] = ~historical_calendar['Day'].isin(['Saturday', 'Sunday'])
    
    # Extended holiday list (simplified for demo - you can add the full list)
    all_holidays = [
    '2007-01-26','2007-03-02','2007-04-06','2007-04-14','2007-05-01','2007-08-15','2007-08-24','2007-10-02','2007-11-09','2007-12-25',
    '2008-01-26','2008-03-06','2008-03-21','2008-04-14','2008-05-01','2008-08-15','2008-09-03','2008-10-02','2008-10-28','2008-12-25',
    '2009-01-26','2009-03-11','2009-04-10','2009-04-14','2009-05-01','2009-08-15','2009-08-23','2009-10-02','2009-10-17','2009-12-25',
    '2010-01-26','2010-03-01','2010-04-02','2010-04-14','2010-05-01','2010-08-15','2010-09-11','2010-10-02','2010-11-05','2010-12-25',
    '2011-01-26','2011-03-19','2011-04-22','2011-04-14','2011-05-01','2011-08-15','2011-09-01','2011-10-02','2011-10-26','2011-12-25',
    '2012-01-26','2012-03-08','2012-04-06','2012-04-14','2012-05-01','2012-08-15','2012-09-19','2012-10-02','2012-11-13','2012-12-25',
    '2013-01-26','2013-03-27','2013-03-29','2013-04-14','2013-05-01','2013-08-15','2013-09-09','2013-10-02','2013-11-03','2013-12-25',
    '2014-01-26','2014-03-17','2014-04-18','2014-04-14','2014-05-01','2014-08-15','2014-08-29','2014-10-02','2014-10-23','2014-12-25',
    '2015-01-26','2015-03-06','2015-04-03','2015-04-14','2015-05-01','2015-08-15','2015-09-17','2015-10-02','2015-11-11','2015-12-25',
    '2016-01-26','2016-03-24','2016-03-25','2016-04-14','2016-05-01','2016-08-15','2016-09-05','2016-10-02','2016-10-30','2016-12-25',
    '2017-01-26','2017-03-13','2017-04-14','2017-04-14','2017-05-01','2017-08-15','2017-08-25','2017-10-02','2017-10-19','2017-12-25',
    '2018-01-26','2018-03-02','2018-03-30','2018-04-14','2018-05-01','2018-08-15','2018-09-13','2018-10-02','2018-11-07','2018-12-25',
    '2019-01-26','2019-03-21','2019-04-19','2019-04-29','2019-04-14','2019-05-01','2019-08-15','2019-09-02','2019-10-02','2019-10-27','2019-12-25',
    '2020-01-26','2020-03-10','2020-04-10','2020-04-14','2020-05-01','2020-08-15','2020-08-22','2020-10-02','2020-11-14','2020-12-25',
    '2021-01-26','2021-03-29','2021-04-02','2021-04-14','2021-05-01','2021-08-15','2021-09-10','2021-10-02','2021-11-04','2021-12-25',
    '2022-01-26','2022-03-18','2022-04-15','2022-04-14','2022-05-01','2022-08-15','2022-08-31','2022-10-02','2022-10-24','2022-12-25',
    '2023-01-26','2023-03-08','2023-04-07','2023-04-14','2023-05-01','2023-08-15','2023-09-19','2023-10-02','2023-11-12','2023-12-25',
    '2024-01-26','2024-03-08','2024-03-25','2024-03-29','2024-04-11','2024-04-14','2024-04-17','2024-05-01','2024-06-17','2024-08-15','2024-09-07','2024-10-02','2024-10-31','2024-11-01','2024-11-15','2024-12-25',
    '2025-01-26','2025-02-26','2025-03-14','2025-03-31','2025-04-06','2025-04-10','2025-04-14','2025-04-18','2025-05-01','2025-06-07','2025-07-06','2025-08-15','2025-08-27','2025-10-02','2025-10-21','2025-10-22','2025-11-05','2025-12-25'
     ]

    
    historical_holiday_dates = pd.to_datetime(all_holidays, errors='coerce')
    historical_calendar.loc[historical_calendar.index.isin(historical_holiday_dates), 'Trading Day'] = False
    
    return historical_calendar



st.markdown("---")
st.markdown("## 📅 Yearly Analysis Dashboard")
st.markdown("*Apply the same filters using yearly last trading day data*")


st.subheader("🔧 Yearly Technical Indicators")

col1, col2, col3, col4 = st.columns(4)
with col1:
    ema_fast = st.number_input("Yearly EMA Fast", min_value=1, max_value=50, value=6, key="y_ema_fast")
with col2:
    ema_slow = st.number_input("Yearly EMA Slow", min_value=1, max_value=100, value=30, key="y_ema_slow")
with col3:
    rsi_period = st.number_input("Yearly RSI Period", min_value=1, max_value=50, value=6, key="y_rsi_period")
with col4:
    rsi_signal = st.number_input("Yearly RSI Signal EMA", min_value=1, max_value=50, value=9, key="y_rsi_signal")


st.subheader("📉 Yearly MACD Settings")
col5, col6, col7 = st.columns(3)
with col5:
    macd_fast = st.number_input("Yearly MACD Fast", min_value=1, max_value=50, value=6, key="y_macd_fast")
with col6:
    macd_slow = st.number_input("Yearly MACD Slow", min_value=1, max_value=100, value=30, key="y_macd_slow")
with col7:
    macd_signal = st.number_input("Yearly MACD Signal", min_value=1, max_value=50, value=9, key="y_macd_signal")



# --- MOVE THIS BLOCK UP: Quarterly Condition UI (main area, like monthly) ---
st.subheader("✅ Yearly Filter Conditions")

col1, col2 = st.columns([3, 1])
with col1:
    use_ema_condition = st.checkbox("Yearly EMA Fast vs EMA Slow", value=True, key="y_ema_cond")
with col2:
    ema_operator = st.selectbox("", [">", "<", ">=", "<=", "=="], key="y_ema_op", label_visibility="collapsed")

col3, col4 = st.columns([3, 1])
with col3:
    use_close_above_ema = st.checkbox("Yearly Close vs EMA Fast", value=True, key="y_close_ema_cond")
with col4:
    close_ema_operator = st.selectbox("", [">", "<", ">=", "<=", "=="], key="y_close_ema_op", label_visibility="collapsed")

col5, col6 = st.columns([3, 1])
with col5:
    use_rsi_condition = st.checkbox("Yearly RSI vs RSI Signal EMA", value=True, key="y_rsi_cond")
with col6:
    rsi_operator = st.selectbox("", [">", "<", ">=", "<=", "=="], key="y_rsi_op", label_visibility="collapsed")

col7, col8 = st.columns([3, 1])
with col7:
    use_macd_condition = st.checkbox("Yearly MACD Line vs MACD Signal", value=True, key="y_macd_cond")
with col8:
    macd_operator = st.selectbox("", [">", "<", ">=", "<=", "=="], key="y_macd_op", label_visibility="collapsed")


def get_yearly_dates(historical_calendar):
    """Get yearly last trading dates"""
    yearly_last_trading_days = []
    for year in range(2008, 2026):
        year_trading = historical_calendar[
            (historical_calendar.index.year == year) & 
            (historical_calendar['Trading Day'] == True)
        ]
        if not year_trading.empty:
            yearly_last_trading_days.append(year_trading.index[-1])


    
    return [d.strftime('%Y-%m-%d') for d in yearly_last_trading_days]

def analyze_stocks(manual_date_dt, ema_fast, ema_slow, rsi_period, rsi_signal,
                  macd_fast, macd_slow, macd_signal, 
                  use_ema_condition, use_close_above_ema, use_rsi_condition, use_macd_condition,
                  ema_operator, close_ema_operator, rsi_operator, macd_operator,
                  ticker_list, yearly_dates):
    
    start_date = start_d
    yearly_filter = []
    stock_data = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, ticker in enumerate(ticker_list):
        status_text.text(f'Analyzing {ticker}... ({i+1}/{len(ticker_list)})')
        progress_bar.progress((i + 1) / len(ticker_list))
        
        try:
            df = yf.download(ticker, start_date, manual_date_dt, interval="1D", progress=False)
            if df.empty:
                continue
                
            df.columns = df.columns.droplevel(1)
            
            yearly_dates_idx = pd.to_datetime(yearly_dates)
            yearly_end_df = df.loc[df.index.intersection(yearly_dates_idx)]
           
            
            if yearly_end_df.empty:
                continue

            yearly_end_df['ema_fast'] = ta.ema(yearly_end_df['Close'], length=ema_fast)
            yearly_end_df['ema_slow'] = ta.ema(yearly_end_df['Close'], length=ema_slow)
            yearly_end_df['rsi'] = ta.rsi(yearly_end_df['Close'], length=rsi_period)
            yearly_end_df['r_ema'] = ta.ema(yearly_end_df['rsi'], length=rsi_signal)
            
            macd = ta.macd(yearly_end_df['Close'], fast=macd_fast, slow=macd_slow, signal=macd_signal)
            yearly_end_df['MACD_Line'] = macd[f'MACD_{macd_fast}_{macd_slow}_{macd_signal}']
            yearly_end_df['MACD_Signal'] = macd[f'MACDs_{macd_fast}_{macd_slow}_{macd_signal}']
            
            yearly = yearly_end_df.tail(1)
            
            if yearly.empty:
                continue
            
            # Helper function to evaluate conditions
            def evaluate_condition(val1, operator, val2):
                if operator == ">":
                    return val1 > val2
                elif operator == "<":
                    return val1 < val2
                elif operator == ">=":
                    return val1 >= val2
                elif operator == "<=":
                    return val1 <= val2
                elif operator == "==":
                    return abs(val1 - val2) < 0.0001  # For floating point comparison
                return False
            
            # Get latest values
            close_val = yearly['Close'].values[0]
            ema_fast_val = yearly['ema_fast'].values[0]
            ema_slow_val = yearly['ema_slow'].values[0]
            rsi_val = yearly['rsi'].values[0]
            r_ema_val = yearly['r_ema'].values[0]
            macd_line_val = yearly['MACD_Line'].values[0]
            macd_signal_val = yearly['MACD_Signal'].values[0]
            
            # Check main conditions
            conditions = []
            condition_details = []
            
            if use_ema_condition:
                cond = evaluate_condition(ema_fast_val, ema_operator, ema_slow_val)
                conditions.append(cond)
                condition_details.append(f"EMA Fast {ema_operator} EMA Slow: {cond} ({ema_fast_val:.2f} {ema_operator} {ema_slow_val:.2f})")
            
            if use_close_above_ema:
                cond = evaluate_condition(close_val, close_ema_operator, ema_fast_val)
                conditions.append(cond)
                condition_details.append(f"Close {close_ema_operator} EMA Fast: {cond} ({close_val:.2f} {close_ema_operator} {ema_fast_val:.2f})")
            
            if use_rsi_condition:
                cond = evaluate_condition(rsi_val, rsi_operator, r_ema_val)
                conditions.append(cond)
                condition_details.append(f"RSI {rsi_operator} RSI Signal: {cond} ({rsi_val:.2f} {rsi_operator} {r_ema_val:.2f})")
            
            if use_macd_condition:
                cond = evaluate_condition(macd_line_val, macd_operator, macd_signal_val)
                conditions.append(cond)
                condition_details.append(f"MACD {macd_operator} MACD Signal: {cond} ({macd_line_val:.4f} {macd_operator} {macd_signal_val:.4f})")
            
           
            passed_filter = all(conditions) if conditions else False
            
            stock_data.append({
                'Ticker': ticker,
                'Close': round(close_val, 2),
                'EMA Fast': round(ema_fast_val, 2),
                'EMA Slow': round(ema_slow_val, 2),
                'RSI': round(rsi_val, 2),
                'RSI Signal': round(r_ema_val, 2),
                'MACD Line': round(macd_line_val, 4),
                'MACD Signal': round(macd_signal_val, 4),
                'Passed Filter': passed_filter,
                'Condition Details': " | ".join(condition_details)
            })

            if passed_filter:
                yearly_filter.append(ticker)
            
            time.sleep(0.1)  # Small delay to avoid rate limiting
            
        except:
            continue
    
    progress_bar.empty()
    status_text.empty()
    
    return yearly_filter, stock_data

# Yearly Analysis Button
if st.button("🚀 Run Yearly Analysis", type="primary", key="yearly_analysis_btn"):
    st.markdown("---")
    
    with st.spinner("Creating trading calendar..."):
        historical_calendar = create_historical_calendar()
        yearly_dates = get_yearly_dates(historical_calendar)
    
    st.success(f"✅ Analysis Date: {manual_date}")
    st.info(f"📊 Analyzing {len(ticker_list)} stocks with the selected parameters")
    
    # Run analysis
    passed_stocks, all_stock_data = analyze_stocks(
        pd.to_datetime(manual_date), ema_fast, ema_slow, rsi_period, rsi_signal,
        macd_fast, macd_slow, macd_signal, 
        use_ema_condition, use_close_above_ema, use_rsi_condition, use_macd_condition,
        ema_operator, close_ema_operator, rsi_operator, macd_operator,
        ticker_list, yearly_dates
    )
    
    # Display results
    if passed_stocks:
        st.subheader("🎯 Filtered Symbols")
        st.markdown("Stock list (one per line):")
        st.code("\n".join(passed_stocks))
        st.download_button(
            label="Download Filtered Symbols (CSV)",
            data="\n".join(passed_stocks),
            file_name="yearly_filtered_symbols.csv",
            mime="text/csv"
        )
        # Changed "Quarterly" to "Yearly" in expander title
        with st.expander("Show Current Yearly Analysis Parameters"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write("**EMA Settings:**")
                st.write(f"- Fast EMA: {ema_fast}")
                st.write(f"- Slow EMA: {ema_slow}")
            with col2:
                st.write("**RSI Settings:**")
                st.write(f"- RSI Period: {rsi_period}")
                st.write(f"- RSI Signal EMA: {rsi_signal}")
            with col3:
                st.write("**MACD Settings:**")
                st.write(f"- Fast: {macd_fast}")
                st.write(f"- Slow: {macd_slow}")
                st.write(f"- Signal: {macd_signal}")
            st.write("**Active Conditions:**")
            conditions_list = []
            if use_ema_condition:
                conditions_list.append(f"EMA Fast {ema_operator} EMA Slow")
            if use_close_above_ema:
                conditions_list.append(f"Close {close_ema_operator} EMA Fast")
            if use_rsi_condition:
                conditions_list.append(f"RSI {rsi_operator} RSI Signal EMA")
            if use_macd_condition:
                conditions_list.append(f"MACD Line {macd_operator} MACD Signal")
            if conditions_list:
                for condition in conditions_list:
                    st.write(f"✅ {condition}")
            else:
                st.write("⚠️ No conditions selected")
    else:
        st.warning("⚠️ No stocks passed the filter criteria")


st.markdown("---")






st.markdown("---")
st.markdown("## 📅 Quarterly Analysis Dashboard")
st.markdown("*Apply the same filters using quarterly last trading day data*")


st.subheader("🔧 Quarterly Technical Indicators")

col1, col2, col3, col4 = st.columns(4)
with col1:
    ema_fast = st.number_input("Quarterly EMA Fast", min_value=1, max_value=50, value=6, key="q_ema_fast")
with col2:
    ema_slow = st.number_input("Quarterly EMA Slow", min_value=1, max_value=100, value=30, key="q_ema_slow")
with col3:
    rsi_period = st.number_input("Quarterly RSI Period", min_value=1, max_value=50, value=6, key="q_rsi_period")
with col4:
    rsi_signal = st.number_input("Quarterly RSI Signal EMA", min_value=1, max_value=50, value=9, key="q_rsi_signal")


st.subheader("📉 Quarterly MACD Settings")
col5, col6, col7 = st.columns(3)
with col5:
    macd_fast = st.number_input("Quarterly MACD Fast", min_value=1, max_value=50, value=6, key="q_macd_fast")
with col6:
    macd_slow = st.number_input("Quarterly MACD Slow", min_value=1, max_value=100, value=30, key="q_macd_slow")
with col7:
    macd_signal = st.number_input("Quarterly MACD Signal", min_value=1, max_value=50, value=9, key="q_macd_signal")



# --- MOVE THIS BLOCK UP: Quarterly Condition UI (main area, like monthly) ---
st.subheader("✅ Quarterly Filter Conditions")

col1, col2 = st.columns([3, 1])
with col1:
    use_ema_condition = st.checkbox("Quarterly EMA Fast vs EMA Slow", value=True, key="q_ema_cond")
with col2:
    ema_operator = st.selectbox("", [">", "<", ">=", "<=", "=="], key="q_ema_op", label_visibility="collapsed")

col3, col4 = st.columns([3, 1])
with col3:
    use_close_above_ema = st.checkbox("Quarterly Close vs EMA Fast", value=True, key="q_close_ema_cond")
with col4:
    close_ema_operator = st.selectbox("", [">", "<", ">=", "<=", "=="], key="q_close_ema_op", label_visibility="collapsed")

col5, col6 = st.columns([3, 1])
with col5:
    use_rsi_condition = st.checkbox("Quarterly RSI vs RSI Signal EMA", value=True, key="q_rsi_cond")
with col6:
    rsi_operator = st.selectbox("", [">", "<", ">=", "<=", "=="], key="q_rsi_op", label_visibility="collapsed")

col7, col8 = st.columns([3, 1])
with col7:
    use_macd_condition = st.checkbox("Quarterly MACD Line vs MACD Signal", value=True, key="q_macd_cond")
with col8:
    macd_operator = st.selectbox("", [">", "<", ">=", "<=", "=="], key="q_macd_op", label_visibility="collapsed")


def get_quarterly_dates(historical_calendar):
    """Get quarterly last trading dates"""
    quarterly_last_trading_days = []
    for year in range(2008, 2026):
        for month in [3, 6, 9, 12]:
            month_trading = historical_calendar[
                (historical_calendar.index.year == year) &
                (historical_calendar.index.month == month) &
                (historical_calendar['Trading Day'] == True)
            ]
            if not month_trading.empty:
                quarterly_last_trading_days.append(month_trading.index[-1])
    
    return [d.strftime('%Y-%m-%d') for d in quarterly_last_trading_days]

def analyze_stocks(manual_date_dt, ema_fast, ema_slow, rsi_period, rsi_signal,
                  macd_fast, macd_slow, macd_signal, 
                  use_ema_condition, use_close_above_ema, use_rsi_condition, use_macd_condition,
                  ema_operator, close_ema_operator, rsi_operator, macd_operator,
                  ticker_list, quarterly_dates):
    
    start_date = start_d
    quarter_filter = []
    stock_data = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, ticker in enumerate(ticker_list):
        status_text.text(f'Analyzing {ticker}... ({i+1}/{len(ticker_list)})')
        progress_bar.progress((i + 1) / len(ticker_list))
        
        try:
            df = yf.download(ticker, start_date, manual_date_dt, interval="1D", progress=False)
            if df.empty:
                continue
                
            df.columns = df.columns.droplevel(1)
            
            quarter_dates_idx = pd.to_datetime(quarterly_dates)
            quarter_end_df = df.loc[df.index.intersection(quarter_dates_idx)]
           
            
            if quarter_end_df.empty:
                continue

            quarter_end_df['ema_fast'] = ta.ema(quarter_end_df['Close'], length=ema_fast)
            quarter_end_df['ema_slow'] = ta.ema(quarter_end_df['Close'], length=ema_slow)
            quarter_end_df['rsi'] = ta.rsi(quarter_end_df['Close'], length=rsi_period)
            quarter_end_df['r_ema'] = ta.ema(quarter_end_df['rsi'], length=rsi_signal)
            
            macd = ta.macd(quarter_end_df['Close'], fast=macd_fast, slow=macd_slow, signal=macd_signal)
            quarter_end_df['MACD_Line'] = macd[f'MACD_{macd_fast}_{macd_slow}_{macd_signal}']
            quarter_end_df['MACD_Signal'] = macd[f'MACDs_{macd_fast}_{macd_slow}_{macd_signal}']
            
            quarter = quarter_end_df.tail(1)
            
            if quarter.empty:
                continue
            
            # Helper function to evaluate conditions
            def evaluate_condition(val1, operator, val2):
                if operator == ">":
                    return val1 > val2
                elif operator == "<":
                    return val1 < val2
                elif operator == ">=":
                    return val1 >= val2
                elif operator == "<=":
                    return val1 <= val2
                elif operator == "==":
                    return abs(val1 - val2) < 0.0001  # For floating point comparison
                return False
            
            # Get latest values
            close_val = quarter['Close'].values[0]
            ema_fast_val = quarter['ema_fast'].values[0]
            ema_slow_val = quarter['ema_slow'].values[0]
            rsi_val = quarter['rsi'].values[0]
            r_ema_val = quarter['r_ema'].values[0]
            macd_line_val = quarter['MACD_Line'].values[0]
            macd_signal_val = quarter['MACD_Signal'].values[0]
            
            # Check main conditions
            conditions = []
            condition_details = []
            
            if use_ema_condition:
                cond = evaluate_condition(ema_fast_val, ema_operator, ema_slow_val)
                conditions.append(cond)
                condition_details.append(f"EMA Fast {ema_operator} EMA Slow: {cond} ({ema_fast_val:.2f} {ema_operator} {ema_slow_val:.2f})")
            
            if use_close_above_ema:
                cond = evaluate_condition(close_val, close_ema_operator, ema_fast_val)
                conditions.append(cond)
                condition_details.append(f"Close {close_ema_operator} EMA Fast: {cond} ({close_val:.2f} {close_ema_operator} {ema_fast_val:.2f})")
            
            if use_rsi_condition:
                cond = evaluate_condition(rsi_val, rsi_operator, r_ema_val)
                conditions.append(cond)
                condition_details.append(f"RSI {rsi_operator} RSI Signal: {cond} ({rsi_val:.2f} {rsi_operator} {r_ema_val:.2f})")
            
            if use_macd_condition:
                cond = evaluate_condition(macd_line_val, macd_operator, macd_signal_val)
                conditions.append(cond)
                condition_details.append(f"MACD {macd_operator} MACD Signal: {cond} ({macd_line_val:.4f} {macd_operator} {macd_signal_val:.4f})")
            
           
            passed_filter = all(conditions) if conditions else False
            
            stock_data.append({
                'Ticker': ticker,
                'Close': round(close_val, 2),
                'EMA Fast': round(ema_fast_val, 2),
                'EMA Slow': round(ema_slow_val, 2),
                'RSI': round(rsi_val, 2),
                'RSI Signal': round(r_ema_val, 2),
                'MACD Line': round(macd_line_val, 4),
                'MACD Signal': round(macd_signal_val, 4),
                'Passed Filter': passed_filter,
                'Condition Details': " | ".join(condition_details)
            })

            if passed_filter:
                quarter_filter.append(ticker)
            
            time.sleep(0.1)  # Small delay to avoid rate limiting
            
        except:
            continue
    
    progress_bar.empty()
    status_text.empty()
    
    return quarter_filter, stock_data

# Quarterly Analysis Button 
if st.button("🚀 Run Quarterly Analysis", type="primary", key="quarterly_analysis_btn"):
    st.markdown("---")
    
    with st.spinner("Creating trading calendar..."):
        historical_calendar = create_historical_calendar()
        quarterly_dates = get_quarterly_dates(historical_calendar)
    
    st.success(f"✅ Analysis Date: {manual_date}")
    st.info(f"📊 Analyzing {len(ticker_list)} stocks with the selected parameters")
    
    # Run analysis
    passed_stocks, all_stock_data = analyze_stocks(
        pd.to_datetime(manual_date), ema_fast, ema_slow, rsi_period, rsi_signal,
        macd_fast, macd_slow, macd_signal, 
        use_ema_condition, use_close_above_ema, use_rsi_condition, use_macd_condition,
        ema_operator, close_ema_operator, rsi_operator, macd_operator,
        ticker_list, quarterly_dates
    )
    
    # Display results
    if passed_stocks:
        st.subheader("🎯 Filtered Symbols")
        st.markdown("Stock list (one per line):")
        st.code("\n".join(passed_stocks))
        st.download_button(
            label="Download Filtered Symbols (CSV)",
            data="\n".join(passed_stocks),
            file_name="quarterly_filtered_symbols.csv",
            mime="text/csv"
        )
        # Show current analysis parameters in an expander
        with st.expander("Show Current Quarterly Analysis Parameters"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write("**EMA Settings:**")
                st.write(f"- Fast EMA: {ema_fast}")
                st.write(f"- Slow EMA: {ema_slow}")
            with col2:
                st.write("**RSI Settings:**")
                st.write(f"- RSI Period: {rsi_period}")
                st.write(f"- RSI Signal EMA: {rsi_signal}")
            with col3:
                st.write("**MACD Settings:**")
                st.write(f"- Fast: {macd_fast}")
                st.write(f"- Slow: {macd_slow}")
                st.write(f"- Signal: {macd_signal}")
            st.write("**Active Conditions:**")
            conditions_list = []
            if use_ema_condition:
                conditions_list.append(f"EMA Fast {ema_operator} EMA Slow")
            if use_close_above_ema:
                conditions_list.append(f"Close {close_ema_operator} EMA Fast")
            if use_rsi_condition:
                conditions_list.append(f"RSI {rsi_operator} RSI Signal EMA")
            if use_macd_condition:
                conditions_list.append(f"MACD Line {macd_operator} MACD Signal")
            if conditions_list:
                for condition in conditions_list:
                    st.write(f"✅ {condition}")
            else:
                st.write("⚠️ No conditions selected")
    else:
        st.warning("⚠️ No stocks passed the filter criteria")


st.markdown("---")





# Add this section after your existing quarterly analysis section
# (around line 300, after the current analysis results display)

st.markdown("---")
st.markdown("## 📅 Monthly Analysis Dashboard")
st.markdown("*Apply the same filters using monthly last trading day data*")

# Monthly Analysis Parameters (separate from quarterly)
st.subheader("🔧 Monthly Technical Indicators")

col1, col2, col3, col4 = st.columns(4)
with col1:
    monthly_ema_fast = st.number_input("Monthly EMA Fast", min_value=1, max_value=50, value=6, key="monthly_ema_fast")
with col2:
    monthly_ema_slow = st.number_input("Monthly EMA Slow", min_value=1, max_value=100, value=30, key="monthly_ema_slow")
with col3:
    monthly_rsi_period = st.number_input("Monthly RSI Period", min_value=1, max_value=50, value=6, key="monthly_rsi_period")
with col4:
    monthly_rsi_signal = st.number_input("Monthly RSI Signal EMA", min_value=1, max_value=50, value=9, key="monthly_rsi_signal")

# Monthly MACD Parameters
st.subheader("📉 Monthly MACD Settings")
col5, col6, col7 = st.columns(3)
with col5:
    monthly_macd_fast = st.number_input("Monthly MACD Fast", min_value=1, max_value=50, value=6, key="monthly_macd_fast")
with col6:
    monthly_macd_slow = st.number_input("Monthly MACD Slow", min_value=1, max_value=100, value=30, key="monthly_macd_slow")
with col7:
    monthly_macd_signal = st.number_input("Monthly MACD Signal", min_value=1, max_value=50, value=9, key="monthly_macd_signal")

# Monthly Condition toggles with operators
st.subheader("✅ Monthly Filter Conditions")

# Monthly EMA Condition
col1, col2 = st.columns([3, 1])
with col1:
    monthly_use_ema_condition = st.checkbox("Monthly EMA Fast vs EMA Slow", value=True, key="monthly_ema_cond")
with col2:
    monthly_ema_operator = st.selectbox("", [">", "<", ">=", "<=", "=="], key="monthly_ema_op", label_visibility="collapsed")

# Monthly Close vs EMA Condition  
col3, col4 = st.columns([3, 1])
with col3:
    monthly_use_close_above_ema = st.checkbox("Monthly Close vs EMA Fast", value=True, key="monthly_close_ema_cond")
with col4:
    monthly_close_ema_operator = st.selectbox("", [">", "<", ">=", "<=", "=="], key="monthly_close_ema_op", label_visibility="collapsed")

# Monthly RSI Condition
col5, col6 = st.columns([3, 1])
with col5:
    monthly_use_rsi_condition = st.checkbox("Monthly RSI vs RSI Signal EMA", value=True, key="monthly_rsi_cond")
with col6:
    monthly_rsi_operator = st.selectbox("", [">", "<", ">=", "<=", "=="], key="monthly_rsi_op", label_visibility="collapsed")

# Monthly MACD Condition
col7, col8 = st.columns([3, 1])
with col7:
    monthly_use_macd_condition = st.checkbox("Monthly MACD Line vs MACD Signal", value=True, key="monthly_macd_cond")
with col8:
    monthly_macd_operator = st.selectbox("", [">", "<", ">=", "<=", "=="], key="monthly_macd_op", label_visibility="collapsed")

def get_monthly_dates(historical_calendar):
    """Get monthly last trading dates"""
    monthly_last_trading_days = []
    for year in range(2008, 2026):
        for month in range(1, 13):
            month_trading = historical_calendar[
                (historical_calendar.index.year == year) &
                (historical_calendar.index.month == month) &
                (historical_calendar['Trading Day'] == True)
            ]
            if not month_trading.empty:
                monthly_last_trading_days.append(month_trading.index[-1])
    
    return [d.strftime('%Y-%m-%d') for d in monthly_last_trading_days]

def analyze_monthly_stocks(manual_date_dt, ema_fast, ema_slow, rsi_period, rsi_signal,
                          macd_fast, macd_slow, macd_signal, 
                          use_ema_condition, use_close_above_ema, use_rsi_condition, use_macd_condition,
                          ema_operator, close_ema_operator, rsi_operator, macd_operator,
                          ticker_list, monthly_dates):
    
    start_date = start_d
    monthly_filter = []
    monthly_stock_data = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, ticker in enumerate(ticker_list):
        status_text.text(f'Analyzing {ticker} (Monthly)... ({i+1}/{len(ticker_list)})')
        progress_bar.progress((i + 1) / len(ticker_list))
        
        try:
            df = yf.download(ticker, start_date, manual_date_dt, interval="1D", progress=False)
            if df.empty:
                continue
                
            df.columns = df.columns.droplevel(1)
            
            month_dates_idx = pd.to_datetime(monthly_dates)
            month_end_df = df.loc[df.index.intersection(month_dates_idx)]
            
            
            if month_end_df.empty:
                continue

            month_end_df['ema_fast'] = ta.ema(month_end_df['Close'], length=ema_fast)
            month_end_df['ema_slow'] = ta.ema(month_end_df['Close'], length=ema_slow)
            month_end_df['rsi'] = ta.rsi(month_end_df['Close'], length=rsi_period)
            month_end_df['r_ema'] = ta.ema(month_end_df['rsi'], length=rsi_signal)
            
            macd = ta.macd(month_end_df['Close'], fast=macd_fast, slow=macd_slow, signal=macd_signal)
            month_end_df['MACD_Line'] = macd[f'MACD_{macd_fast}_{macd_slow}_{macd_signal}']
            month_end_df['MACD_Signal'] = macd[f'MACDs_{macd_fast}_{macd_slow}_{macd_signal}']
            
            monthly = month_end_df.tail(1)
            
            if monthly.empty:
                continue
            
            # Helper function to evaluate conditions
            def evaluate_condition(val1, operator, val2):
                if operator == ">":
                    return val1 > val2
                elif operator == "<":
                    return val1 < val2
                elif operator == ">=":
                    return val1 >= val2
                elif operator == "<=":
                    return val1 <= val2
                elif operator == "==":
                    return abs(val1 - val2) < 0.0001  # For floating point comparison
                return False
            
            # Get latest values
            close_val = monthly['Close'].values[0]
            ema_fast_val = monthly['ema_fast'].values[0]
            ema_slow_val = monthly['ema_slow'].values[0]
            rsi_val = monthly['rsi'].values[0]
            r_ema_val = monthly['r_ema'].values[0]
            macd_line_val = monthly['MACD_Line'].values[0]
            macd_signal_val = monthly['MACD_Signal'].values[0]
            
            # Check main conditions
            conditions = []
            condition_details = []
            
            if use_ema_condition:
                cond = evaluate_condition(ema_fast_val, ema_operator, ema_slow_val)
                conditions.append(cond)
                condition_details.append(f"EMA Fast {ema_operator} EMA Slow: {cond} ({ema_fast_val:.2f} {ema_operator} {ema_slow_val:.2f})")
            
            if use_close_above_ema:
                cond = evaluate_condition(close_val, close_ema_operator, ema_fast_val)
                conditions.append(cond)
                condition_details.append(f"Close {close_ema_operator} EMA Fast: {cond} ({close_val:.2f} {close_ema_operator} {ema_fast_val:.2f})")
            
            if use_rsi_condition:
                cond = evaluate_condition(rsi_val, rsi_operator, r_ema_val)
                conditions.append(cond)
                condition_details.append(f"RSI {rsi_operator} RSI Signal: {cond} ({rsi_val:.2f} {rsi_operator} {r_ema_val:.2f})")
            
            if use_macd_condition:
                cond = evaluate_condition(macd_line_val, macd_operator, macd_signal_val)
                conditions.append(cond)
                condition_details.append(f"MACD {macd_operator} MACD Signal: {cond} ({macd_line_val:.4f} {macd_operator} {macd_signal_val:.4f})")
            
            passed_filter = all(conditions) if conditions else False
            
            monthly_stock_data.append({
                'Ticker': ticker,
                'Close': round(close_val, 2),
                'EMA Fast': round(ema_fast_val, 2),
                'EMA Slow': round(ema_slow_val, 2),
                'RSI': round(rsi_val, 2),
                'RSI Signal': round(r_ema_val, 2),
                'MACD Line': round(macd_line_val, 4),
                'MACD Signal': round(macd_signal_val, 4),
                'Passed Filter': passed_filter,
                'Condition Details': " | ".join(condition_details)
            })

            if passed_filter:
                monthly_filter.append(ticker)
            
            time.sleep(0.1)  # Small delay to avoid rate limiting
            
        except:
            continue
    
    progress_bar.empty()
    status_text.empty()
    
    return monthly_filter, monthly_stock_data

# Monthly Analysis Button
if st.button("🚀 Run Monthly Analysis", type="primary", key="monthly_analysis_btn"):
    st.markdown("---")
    
    with st.spinner("Creating monthly trading calendar..."):
        historical_calendar = create_historical_calendar()
        monthly_dates = get_monthly_dates(historical_calendar)
    
    st.success(f"✅ Monthly Analysis Date: {manual_date}")
    st.info(f"📊 Analyzing {len(ticker_list)} stocks with monthly parameters")
    
    # Run monthly analysis
    passed_monthly_stocks, all_monthly_stock_data = analyze_monthly_stocks(
        pd.to_datetime(manual_date), monthly_ema_fast, monthly_ema_slow, monthly_rsi_period, monthly_rsi_signal,
        monthly_macd_fast, monthly_macd_slow, monthly_macd_signal, 
        monthly_use_ema_condition, monthly_use_close_above_ema, monthly_use_rsi_condition, monthly_use_macd_condition,
        monthly_ema_operator, monthly_close_ema_operator, monthly_rsi_operator, monthly_macd_operator,
        ticker_list, monthly_dates
    )
    
    # Display monthly results
    if passed_monthly_stocks:
        st.subheader("🎯 Monthly Filtered Symbols")
        st.markdown("Stock list (one per line):")
        st.code("\n".join(passed_monthly_stocks))
        st.download_button(
            label="Download Monthly Filtered Symbols (CSV)",
            data="\n".join(passed_monthly_stocks),
            file_name="monthly_filtered_symbols.csv",
            mime="text/csv"
        )
        # Display detailed results in a table
        if st.checkbox("Show Monthly Analysis Details", key="monthly_details"):
            monthly_df = pd.DataFrame(all_monthly_stock_data)
            monthly_passed_df = monthly_df[monthly_df['Passed Filter'] == True]
            
            if not monthly_passed_df.empty:
                st.subheader("📊 Monthly Passed Stocks Details")
                st.dataframe(monthly_passed_df, use_container_width=True)
            
            if st.checkbox("Show All Monthly Analysis Data", key="monthly_all_data"):
                st.subheader("📋 All Monthly Stocks Analysis")
                st.dataframe(monthly_df, use_container_width=True)
    else:
        st.warning("⚠️ No stocks passed the monthly filter criteria")

# Display current monthly parameters
with st.expander("🔍 Current Monthly Analysis Parameters"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Monthly EMA Settings:**")
        st.write(f"- Fast EMA: {monthly_ema_fast}")
        st.write(f"- Slow EMA: {monthly_ema_slow}")
    
    with col2:
        st.write("**Monthly RSI Settings:**")
        st.write(f"- RSI Period: {monthly_rsi_period}")
        st.write(f"- RSI Signal EMA: {monthly_rsi_signal}")
    
    with col3:
        st.write("**Monthly MACD Settings:**")
        st.write(f"- Fast: {monthly_macd_fast}")
        st.write(f"- Slow: {monthly_macd_slow}")
        st.write(f"- Signal: {monthly_macd_signal}")
    
    st.write("**Active Monthly Conditions:**")
    monthly_conditions_list = []
    if monthly_use_ema_condition:
        monthly_conditions_list.append(f"EMA Fast {monthly_ema_operator} EMA Slow")
    if monthly_use_close_above_ema:
        monthly_conditions_list.append(f"Close {monthly_close_ema_operator} EMA Fast")
    if monthly_use_rsi_condition:
        monthly_conditions_list.append(f"RSI {monthly_rsi_operator} RSI Signal EMA")
    if monthly_use_macd_condition:
        monthly_conditions_list.append(f"MACD Line {monthly_macd_operator} MACD Signal")
    
    if monthly_conditions_list:
        for condition in monthly_conditions_list:
            st.write(f"✅ {condition}")
    else:
        st.write("⚠️ No monthly conditions selected")

# Comparison section between quarterly and monthly results
st.markdown("---")
st.markdown("## 📅 Weekly Analysis Dashboard")
st.markdown("*Apply the same filters using weekly last trading day data*")

# Weekly Analysis Parameters (separate from quarterly and monthly)
st.subheader("🔧 Weekly Technical Indicators")

col1, col2, col3, col4 = st.columns(4)
with col1:
    weekly_ema_fast = st.number_input("Weekly EMA Fast", min_value=1, max_value=50, value=6, key="weekly_ema_fast")
with col2:
    weekly_ema_slow = st.number_input("Weekly EMA Slow", min_value=1, max_value=100, value=30, key="weekly_ema_slow")
with col3:
    weekly_rsi_period = st.number_input("Weekly RSI Period", min_value=1, max_value=50, value=6, key="weekly_rsi_period")
with col4:
    weekly_rsi_signal = st.number_input("Weekly RSI Signal EMA", min_value=1, max_value=50, value=9, key="weekly_rsi_signal")

# Weekly MACD Parameters
st.subheader("📉 Weekly MACD Settings")
col5, col6, col7 = st.columns(3)
with col5:
    weekly_macd_fast = st.number_input("Weekly MACD Fast", min_value=1, max_value=50, value=6, key="weekly_macd_fast")
with col6:
    weekly_macd_slow = st.number_input("Weekly MACD Slow", min_value=1, max_value=100, value=30, key="weekly_macd_slow")
with col7:
    weekly_macd_signal = st.number_input("Weekly MACD Signal", min_value=1, max_value=50, value=9, key="weekly_macd_signal")

# Weekly Condition toggles with operators
st.subheader("✅ Weekly Filter Conditions")

# Weekly EMA Condition
col1, col2 = st.columns([3, 1])
with col1:
    weekly_use_ema_condition = st.checkbox("Weekly EMA Fast vs EMA Slow", value=True, key="weekly_ema_cond")
with col2:
    weekly_ema_operator = st.selectbox("", [">", "<", ">=", "<=", "=="], index=1, key="weekly_ema_op", label_visibility="collapsed")

# Weekly Close vs EMA Condition  
col3, col4 = st.columns([3, 1])
with col3:
    weekly_use_close_above_ema = st.checkbox("Weekly Close vs EMA Fast", value=True, key="weekly_close_ema_cond")
with col4:
    weekly_close_ema_operator = st.selectbox("", [">", "<", ">=", "<=", "=="], index=1, key="weekly_close_ema_op", label_visibility="collapsed")

# Weekly RSI Condition
col5, col6 = st.columns([3, 1])
with col5:
    weekly_use_rsi_condition = st.checkbox("Weekly RSI vs RSI Signal EMA", value=True, key="weekly_rsi_cond")
with col6:
    weekly_rsi_operator = st.selectbox("", [">", "<", ">=", "<=", "=="], key="weekly_rsi_op", label_visibility="collapsed")

# Weekly MACD Condition
col7, col8 = st.columns([3, 1])
with col7:
    weekly_use_macd_condition = st.checkbox("Weekly MACD Line vs MACD Signal", value=True, key="weekly_macd_cond")
with col8:
    weekly_macd_operator = st.selectbox("", [">", "<", ">=", "<=", "=="], index=1, key="weekly_macd_op", label_visibility="collapsed")

def get_weekly_dates(historical_calendar):
    """Get weekly last trading dates"""
    weekly_last_trading_days = []
    all_dates = historical_calendar[historical_calendar['Trading Day'] == True].index
    
    for year in range(2008, 2026):
        for week in range(1, 54):
            week_days = [d for d in all_dates if d.isocalendar()[0] == year and d.isocalendar()[1] == week]
            if week_days:
                weekly_last_trading_days.append(week_days[-1])
    
    return [d.strftime('%Y-%m-%d') for d in weekly_last_trading_days]

def analyze_weekly_stocks(manual_date_dt, ema_fast, ema_slow, rsi_period, rsi_signal,
                         macd_fast, macd_slow, macd_signal, 
                         use_ema_condition, use_close_above_ema, use_rsi_condition, use_macd_condition,
                         ema_operator, close_ema_operator, rsi_operator, macd_operator,
                         ticker_list, weekly_dates):
    
    start_date = start_d
    weekly_filter = []
    weekly_stock_data = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, ticker in enumerate(ticker_list):
        status_text.text(f'Analyzing {ticker} (Weekly)... ({i+1}/{len(ticker_list)})')
        progress_bar.progress((i + 1) / len(ticker_list))
        
        try:
            df = yf.download(ticker, start_date, manual_date_dt, interval="1D", progress=False)
            if df.empty:
                continue
                
            df.columns = df.columns.droplevel(1)
            
            week_dates_idx = pd.to_datetime(weekly_dates)
            week_end_df = df.loc[df.index.intersection(week_dates_idx)]
            
            
            if week_end_df.empty:
                continue

            week_end_df['ema_fast'] = ta.ema(week_end_df['Close'], length=ema_fast)
            week_end_df['ema_slow'] = ta.ema(week_end_df['Close'], length=ema_slow)
            week_end_df['rsi'] = ta.rsi(week_end_df['Close'], length=rsi_period)
            week_end_df['r_ema'] = ta.ema(week_end_df['rsi'], length=rsi_signal)
            
            macd = ta.macd(week_end_df['Close'], fast=macd_fast, slow=macd_slow, signal=macd_signal)
            week_end_df['MACD_Line'] = macd[f'MACD_{macd_fast}_{macd_slow}_{macd_signal}']
            week_end_df['MACD_Signal'] = macd[f'MACDs_{macd_fast}_{macd_slow}_{macd_signal}']
            
            weekly = week_end_df.tail(1)
            
            if weekly.empty:
                continue
            
            # Helper function to evaluate conditions
            def evaluate_condition(val1, operator, val2):
                if operator == ">":
                    return val1 > val2
                elif operator == "<":
                    return val1 < val2
                elif operator == ">=":
                    return val1 >= val2
                elif operator == "<=":
                    return val1 <= val2
                elif operator == "==":
                    return abs(val1 - val2) < 0.0001  # For floating point comparison
                return False
            
            # Get latest values
            close_val = weekly['Close'].values[0]
            ema_fast_val = weekly['ema_fast'].values[0]
            ema_slow_val = weekly['ema_slow'].values[0]
            rsi_val = weekly['rsi'].values[0]
            r_ema_val = weekly['r_ema'].values[0]
            macd_line_val = weekly['MACD_Line'].values[0]
            macd_signal_val = weekly['MACD_Signal'].values[0]
            
            # Check main conditions
            conditions = []
            condition_details = []
            
            if use_ema_condition:
                cond = evaluate_condition(ema_fast_val, ema_operator, ema_slow_val)
                conditions.append(cond)
                condition_details.append(f"EMA Fast {ema_operator} EMA Slow: {cond} ({ema_fast_val:.2f} {ema_operator} {ema_slow_val:.2f})")
            
            if use_close_above_ema:
                cond = evaluate_condition(close_val, close_ema_operator, ema_fast_val)
                conditions.append(cond)
                condition_details.append(f"Close {close_ema_operator} EMA Fast: {cond} ({close_val:.2f} {close_ema_operator} {ema_fast_val:.2f})")
            
            if use_rsi_condition:
                cond = evaluate_condition(rsi_val, rsi_operator, r_ema_val)
                conditions.append(cond)
                condition_details.append(f"RSI {rsi_operator} RSI Signal: {cond} ({rsi_val:.2f} {rsi_operator} {r_ema_val:.2f})")
            
            if use_macd_condition:
                cond = evaluate_condition(macd_line_val, macd_operator, macd_signal_val)
                conditions.append(cond)
                condition_details.append(f"MACD {macd_operator} MACD Signal: {cond} ({macd_line_val:.4f} {macd_operator} {macd_signal_val:.4f})")
            
            passed_filter = all(conditions) if conditions else False
            
            weekly_stock_data.append({
                'Ticker': ticker,
                'Close': round(close_val, 2),
                'EMA Fast': round(ema_fast_val, 2),
                'EMA Slow': round(ema_slow_val, 2),
                'RSI': round(rsi_val, 2),
                'RSI Signal': round(r_ema_val, 2),
                'MACD Line': round(macd_line_val, 4),
                'MACD Signal': round(macd_signal_val, 4),
                'Passed Filter': passed_filter,
                'Condition Details': " | ".join(condition_details)
            })

            if passed_filter:
                weekly_filter.append(ticker)
            
            time.sleep(0.1)  # Small delay to avoid rate limiting
            
        except:
            continue
    
    progress_bar.empty()
    status_text.empty()
    
    return weekly_filter, weekly_stock_data

# Weekly Analysis Button
if st.button("🚀 Run Weekly Analysis", type="primary", key="weekly_analysis_btn"):
    st.markdown("---")
    
    with st.spinner("Creating weekly trading calendar..."):
        historical_calendar = create_historical_calendar()
        weekly_dates = get_weekly_dates(historical_calendar)
    
    st.success(f"✅ Weekly Analysis Date: {manual_date}")
    st.info(f"📊 Analyzing {len(ticker_list)} stocks with weekly parameters")
    
    # Run weekly analysis
    passed_weekly_stocks, all_weekly_stock_data = analyze_weekly_stocks(
        pd.to_datetime(manual_date), weekly_ema_fast, weekly_ema_slow, weekly_rsi_period, weekly_rsi_signal,
        weekly_macd_fast, weekly_macd_slow, weekly_macd_signal, 
        weekly_use_ema_condition, weekly_use_close_above_ema, weekly_use_rsi_condition, weekly_use_macd_condition,
        weekly_ema_operator, weekly_close_ema_operator, weekly_rsi_operator, weekly_macd_operator,
        ticker_list, weekly_dates
    )
    
    # Display weekly results
    if passed_weekly_stocks:
        st.subheader("🎯 Weekly Filtered Symbols")
        st.markdown("Stock list (one per line):")
        st.code("\n".join(passed_weekly_stocks))
        st.download_button(
            label="Download Weekly Filtered Symbols (CSV)",
            data="\n".join(passed_weekly_stocks),
            file_name="weekly_filtered_symbols.csv",
            mime="text/csv"
        )
        # Display detailed results in a table
        if st.checkbox("Show Weekly Analysis Details", key="weekly_details"):
            weekly_df = pd.DataFrame(all_weekly_stock_data)
            weekly_passed_df = weekly_df[weekly_df['Passed Filter'] == True]
            
            if not weekly_passed_df.empty:
                st.subheader("📊 Weekly Passed Stocks Details")
                st.dataframe(weekly_passed_df, use_container_width=True)
            
            if st.checkbox("Show All Weekly Analysis Data", key="weekly_all_data"):
                st.subheader("📋 All Weekly Stocks Analysis")
                st.dataframe(weekly_df, use_container_width=True)
    else:
        st.warning("⚠️ No stocks passed the weekly filter criteria")

# Display current weekly parameters
with st.expander("🔍 Current Weekly Analysis Parameters"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Weekly EMA Settings:**")
        st.write(f"- Fast EMA: {weekly_ema_fast}")
        st.write(f"- Slow EMA: {weekly_ema_slow}")
    
    with col2:
        st.write("**Weekly RSI Settings:**")
        st.write(f"- RSI Period: {weekly_rsi_period}")
        st.write(f"- RSI Signal EMA: {weekly_rsi_signal}")
    
    with col3:
        st.write("**Weekly MACD Settings:**")
        st.write(f"- Fast: {weekly_macd_fast}")
        st.write(f"- Slow: {weekly_macd_slow}")
        st.write(f"- Signal: {weekly_macd_signal}")
    
    st.write("**Active Weekly Conditions:**")
    weekly_conditions_list = []
    if weekly_use_ema_condition:
        weekly_conditions_list.append(f"EMA Fast {weekly_ema_operator} EMA Slow")
    if weekly_use_close_above_ema:
        weekly_conditions_list.append(f"Close {weekly_close_ema_operator} EMA Fast")
    if weekly_use_rsi_condition:
        weekly_conditions_list.append(f"RSI {weekly_rsi_operator} RSI Signal EMA")
    if weekly_use_macd_condition:
        weekly_conditions_list.append(f"MACD Line {weekly_macd_operator} MACD Signal")
    
    if weekly_conditions_list:
        for condition in weekly_conditions_list:
            st.write(f"✅ {condition}")
    else:
        st.write("⚠️ No weekly conditions selected")

# Comparison section between quarterly, monthly, and weekly results
st.markdown("---")
st.markdown("## 📅 Daily Analysis Dashboard")
st.markdown("*Apply the same filters using daily data (most recent trading day)*")

# Daily Analysis Parameters (separate from quarterly, monthly, and weekly)
st.subheader("🔧 Daily Technical Indicators")

col1, col2, col3, col4 = st.columns(4)
with col1:
    daily_ema_fast = st.number_input("Daily EMA Fast", min_value=1, max_value=50, value=6, key="daily_ema_fast")
with col2:
    daily_ema_slow = st.number_input("Daily EMA Slow", min_value=1, max_value=100, value=30, key="daily_ema_slow")
with col3:
    daily_rsi_period = st.number_input("Daily RSI Period", min_value=1, max_value=50, value=6, key="daily_rsi_period")
with col4:
    daily_rsi_signal = st.number_input("Daily RSI Signal EMA", min_value=1, max_value=50, value=9, key="daily_rsi_signal")

# Daily MACD Parameters
st.subheader("📉 Daily MACD Settings")
col5, col6, col7 = st.columns(3)
with col5:
    daily_macd_fast = st.number_input("Daily MACD Fast", min_value=1, max_value=50, value=6, key="daily_macd_fast")
with col6:
    daily_macd_slow = st.number_input("Daily MACD Slow", min_value=1, max_value=100, value=30, key="daily_macd_slow")
with col7:
    daily_macd_signal = st.number_input("Daily MACD Signal", min_value=1, max_value=50, value=9, key="daily_macd_signal")

# Daily Condition toggles with operators
st.subheader("✅ Daily Filter Conditions")

# Daily EMA Condition
col1, col2 = st.columns([3, 1])
with col1:
    daily_use_ema_condition = st.checkbox("Daily EMA Fast vs EMA Slow", value=True, key="daily_ema_cond")
with col2:
    daily_ema_operator = st.selectbox("", [">", "<", ">=", "<=", "=="], index=1, key="daily_ema_op", label_visibility="collapsed")

# Daily Close vs EMA Condition  
col3, col4 = st.columns([3, 1])
with col3:
    daily_use_close_above_ema = st.checkbox("Daily Close vs EMA Fast", value=True, key="daily_close_ema_cond")
with col4:
    daily_close_ema_operator = st.selectbox("", [">", "<", ">=", "<=", "=="], index=1, key="daily_close_ema_op", label_visibility="collapsed")

# Daily RSI Condition
col5, col6 = st.columns([3, 1])
with col5:
    daily_use_rsi_condition = st.checkbox("Daily RSI vs RSI Signal EMA", value=True, key="daily_rsi_cond")
with col6:
    daily_rsi_operator = st.selectbox("", [">", "<", ">=", "<=", "=="], key="daily_rsi_op", label_visibility="collapsed")

# Daily MACD Condition
col7, col8 = st.columns([3, 1])
with col7:
    daily_use_macd_condition = st.checkbox("Daily MACD Line vs MACD Signal", value=True, key="daily_macd_cond")
with col8:
    daily_macd_operator = st.selectbox("", [">", "<", ">=", "<=", "=="], key="daily_macd_op", label_visibility="collapsed")

def analyze_daily_stocks(manual_date_dt, ema_fast, ema_slow, rsi_period, rsi_signal,
                        macd_fast, macd_slow, macd_signal, 
                        use_ema_condition, use_close_above_ema, use_rsi_condition, use_macd_condition,
                        ema_operator, close_ema_operator, rsi_operator, macd_operator,
                        ticker_list):
    
    start_date = start_d
    daily_filter = []
    daily_stock_data = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, ticker in enumerate(ticker_list):
        status_text.text(f'Analyzing {ticker} (Daily)... ({i+1}/{len(ticker_list)})')
        progress_bar.progress((i + 1) / len(ticker_list))
        
        try:
            df = yf.download(ticker, start_date, manual_date_dt, interval="1d", progress=False)
            if df.empty:
                continue
                
            df.columns = df.columns.droplevel(1)
            
            # Calculate technical indicators for daily data
            df['ema_fast'] = ta.ema(df['Close'], length=ema_fast)
            df['ema_slow'] = ta.ema(df['Close'], length=ema_slow)
            df['rsi'] = ta.rsi(df['Close'], length=rsi_period)
            df['r_ema'] = ta.ema(df['rsi'], length=rsi_signal)
            
            macd = ta.macd(df['Close'], fast=macd_fast, slow=macd_slow, signal=macd_signal)
            df['MACD_Line'] = macd[f'MACD_{macd_fast}_{macd_slow}_{macd_signal}']
            df['MACD_Signal'] = macd[f'MACDs_{macd_fast}_{macd_slow}_{macd_signal}']
            df['MACD_Hist'] = macd[f'MACDh_{macd_fast}_{macd_slow}_{macd_signal}']
            df['MACD_Level'] = df['MACD_Line'] - df['MACD_Signal']
            
            # Get the most recent daily data
            daily = df.tail(1)
            
            if daily.empty:
                continue
            
            # Helper function to evaluate conditions
            def evaluate_condition(val1, operator, val2):
                if operator == ">":
                    return val1 > val2
                elif operator == "<":
                    return val1 < val2
                elif operator == ">=":
                    return val1 >= val2
                elif operator == "<=":
                    return val1 <= val2
                elif operator == "==":
                    return abs(val1 - val2) < 0.0001  # For floating point comparison
                return False
            
            # Get latest values
            close_val = daily['Close'].values[0]
            ema_fast_val = daily['ema_fast'].values[0]
            ema_slow_val = daily['ema_slow'].values[0]
            rsi_val = daily['rsi'].values[0]
            r_ema_val = daily['r_ema'].values[0]
            macd_line_val = daily['MACD_Line'].values[0]
            macd_signal_val = daily['MACD_Signal'].values[0]
            macd_hist_val = daily['MACD_Hist'].values[0]
            macd_level_val = daily['MACD_Level'].values[0]
            
            # Check main conditions
            conditions = []
            condition_details = []
            
            if use_ema_condition:
                cond = evaluate_condition(ema_fast_val, ema_operator, ema_slow_val)
                conditions.append(cond)
                condition_details.append(f"EMA Fast {ema_operator} EMA Slow: {cond} ({ema_fast_val:.2f} {ema_operator} {ema_slow_val:.2f})")
            
            if use_close_above_ema:
                cond = evaluate_condition(close_val, close_ema_operator, ema_fast_val)
                conditions.append(cond)
                condition_details.append(f"Close {close_ema_operator} EMA Fast: {cond} ({close_val:.2f} {close_ema_operator} {ema_fast_val:.2f})")
            
            if use_rsi_condition:
                cond = evaluate_condition(rsi_val, rsi_operator, r_ema_val)
                conditions.append(cond)
                condition_details.append(f"RSI {rsi_operator} RSI Signal: {cond} ({rsi_val:.2f} {rsi_operator} {r_ema_val:.2f})")
            
            if use_macd_condition:
                cond = evaluate_condition(macd_line_val, macd_operator, macd_signal_val)
                conditions.append(cond)
                condition_details.append(f"MACD {macd_operator} MACD Signal: {cond} ({macd_line_val:.4f} {macd_operator} {macd_signal_val:.4f})")
            
            passed_filter = all(conditions) if conditions else False
            
            daily_stock_data.append({
                'Ticker': ticker,
                'Close': round(close_val, 2),
                'EMA Fast': round(ema_fast_val, 2),
                'EMA Slow': round(ema_slow_val, 2),
                'RSI': round(rsi_val, 2),
                'RSI Signal': round(r_ema_val, 2),
                'MACD Line': round(macd_line_val, 4),
                'MACD Signal': round(macd_signal_val, 4),
                'MACD Hist': round(macd_hist_val, 4),
                'MACD Level': round(macd_level_val, 4),
                'Passed Filter': passed_filter,
                'Condition Details': " | ".join(condition_details)
            })

            if passed_filter:
                daily_filter.append(ticker)
            
            time.sleep(0.1)  # Small delay to avoid rate limiting
            
        except:
            continue
    
    progress_bar.empty()
    status_text.empty()
    
    return daily_filter, daily_stock_data

# Daily Analysis Button  
if st.button("🚀 Run Daily Analysis", type="primary", key="daily_analysis_btn"):
    st.markdown("---")
    
    st.success(f"✅ Daily Analysis Date: {manual_date}")
    st.info(f"📊 Analyzing {len(ticker_list)} stocks with daily parameters")
    
    # Run daily analysis
    passed_daily_stocks, all_daily_stock_data = analyze_daily_stocks(
        pd.to_datetime(manual_date), daily_ema_fast, daily_ema_slow, daily_rsi_period, daily_rsi_signal,
        daily_macd_fast, daily_macd_slow, daily_macd_signal, 
        daily_use_ema_condition, daily_use_close_above_ema, daily_use_rsi_condition, daily_use_macd_condition,
        daily_ema_operator, daily_close_ema_operator, daily_rsi_operator, daily_macd_operator,
        ticker_list
    )
    
    # Display daily results
    if passed_daily_stocks:
        st.subheader("🎯 Daily Filtered Symbols")
        st.markdown("Stock list (one per line):")
        st.code("\n".join(passed_daily_stocks))
        st.download_button(
            label="Download Daily Filtered Symbols (CSV)",
            data="\n".join(passed_daily_stocks),
            file_name="daily_filtered_symbols.csv",
            mime="text/csv"
        )
        # Display detailed results in a table
        if st.checkbox("Show Daily Analysis Details", key="daily_details"):
            daily_df = pd.DataFrame(all_daily_stock_data)
            daily_passed_df = daily_df[daily_df['Passed Filter'] == True]
            
            if not daily_passed_df.empty:
                st.subheader("📊 Daily Passed Stocks Details")
                st.dataframe(daily_passed_df, use_container_width=True)
            
            if st.checkbox("Show All Daily Analysis Data", key="daily_all_data"):
                st.subheader("📋 All Daily Stocks Analysis")
                st.dataframe(daily_df, use_container_width=True)
    else:
        st.warning("⚠️ No stocks passed the daily filter criteria")

# Display current daily parameters
with st.expander("🔍 Current Daily Analysis Parameters"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Daily EMA Settings:**")
        st.write(f"- Fast EMA: {daily_ema_fast}")
        st.write(f"- Slow EMA: {daily_ema_slow}")
    
    with col2:
        st.write("**Daily RSI Settings:**")
        st.write(f"- RSI Period: {daily_rsi_period}")
        st.write(f"- RSI Signal EMA: {daily_rsi_signal}")
    
    with col3:
        st.write("**Daily MACD Settings:**")
        st.write(f"- Fast: {daily_macd_fast}")
        st.write(f"- Slow: {daily_macd_slow}")
        st.write(f"- Signal: {daily_macd_signal}")
    
    st.write("**Active Daily Conditions:**")
    daily_conditions_list = []
    if daily_use_ema_condition:
        daily_conditions_list.append(f"EMA Fast {daily_ema_operator} EMA Slow")
    if daily_use_close_above_ema:
        daily_conditions_list.append(f"Close {daily_close_ema_operator} EMA Fast")
    if daily_use_rsi_condition:
        daily_conditions_list.append(f"RSI {daily_rsi_operator} RSI Signal EMA")
    if daily_use_macd_condition:
        daily_conditions_list.append(f"MACD Line {daily_macd_operator} MACD Signal")
    
    if daily_conditions_list:
        for condition in daily_conditions_list:
            st.write(f"✅ {condition}")
    else:
        st.write("⚠️ No daily conditions selected")

# Final comparison section for all timeframes
st.markdown("---")


# You can add comprehensive comparison logic here when all analyses have been run












# Trading Analysis Dashboard with Dropdown Selection


# Add dropdown menu for analysis selection
st.markdown("## 📊 Indicators Dashboard")
st.markdown("*Select your preferred analysis method from the dropdown below*")

# Dropdown menu for analysis selection
analysis_options = [
    
    "Daily Bollinger Bands",
    "Weekly Bollinger Bands", 
    "Daily Supertrend",
    "Weekly Supertrend",
    "Daily Linear Regression",
    "Weekly Linear Regression"
]

selected_analysis = st.selectbox("Choose Analysis Type:", analysis_options)

# Show analysis based on selection
if selected_analysis == "Daily Bollinger Bands":
    st.markdown("---")
    st.markdown("## 📅 Daily Bollinger Analysis Dashboard")
    st.markdown("*Apply bollinger filters using daily data (most recent trading day)*")
    
    # Bollinger Analysis Parameters
    st.subheader("🔧 Bollinger Parameters")
    col1, col2, col3 = st.columns(3)
    with col1:
        length = st.number_input("Bollinger Period", min_value=1, max_value=50, value=20, key="daily_bollinger_period")
    with col2:
        std = st.number_input("Bollinger Multiplier", min_value=0.1, max_value=10.0, value=2.0, step=0.1, key="daily_bollinger_multiplier")

    def calculate_bollinger(df, length, std):
        """Calculate bollinger indicator using pandas_ta"""
        bb = ta.bbands(close=df['Close'], length=length, std=std)
        bb['Close'] = df['Close']
        return bb

    def analyze_bollinger_stocks(manual_date_dt, length, std, ticker_list):
        start_date = start_d
        bollinger_filter = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        last_df = None

        for i, ticker in enumerate(ticker_list):
            try:
                status_text.text(f'Analyzing {ticker} (bollinger)... ({i+1}/{len(ticker_list)})')
                progress_bar.progress((i + 1) / len(ticker_list))

                try:
                    df = yf.download(ticker, start_date, manual_date_dt, interval="1d", progress=False)
                    time.sleep(0.1)
            
                    if df.empty:
                        continue
                    df.columns = df.columns.droplevel(1)
                    
                    last_df = calculate_bollinger(df, length, std)
                except:
                    continue
                
                column_name = f'BBL_{length}_{float(std):.1f}'
                if (last_df['Close'][-2] < last_df[column_name][-2]) and (last_df['Close'][-1] > last_df[column_name][-1]):
                    bollinger_filter.append(ticker)
                else:
                    continue
            except:
                continue

        return bollinger_filter

    if st.button('Run Daily Bollinger Analysis'): 
        bollinger_stocks = analyze_bollinger_stocks(manual_date, length, std, ticker_list)
        st.write(bollinger_stocks)

        if bollinger_stocks:
            st.subheader("🎯 Bollinger Filtered Symbols")
            st.markdown("Stock list (one per line):")
            st.code("\n".join(bollinger_stocks))
            st.download_button(
                label="Download Bollinger Filtered Symbols (CSV)",
                data="\n".join(bollinger_stocks),
                file_name="daily_bollinger_filtered_symbols.csv",
                mime="text/csv"
            )
        else:
            st.warning("⚠️ No stocks passed the daily bollinger filter criteria")

elif selected_analysis == "Weekly Bollinger Bands":
    st.markdown("---")
    st.markdown("## 📅 Weekly Bollinger Analysis Dashboard")
    st.markdown("*Apply bollinger filters using weekly data*")
    
    # Bollinger Analysis Parameters
    st.subheader("🔧 Bollinger Parameters")
    col1, col2, col3 = st.columns(3)
    with col1:
        length = st.number_input("Bollinger Period", min_value=1, max_value=50, value=20, key="weekly_bollinger_period")
    with col2:
        std = st.number_input("Bollinger Multiplier", min_value=0.1, max_value=10.0, value=2.0, step=0.1, key="weekly_bollinger_multiplier")

    def get_weekly_dates(historical_calendar):
        """Get weekly last trading dates"""
        weekly_last_trading_days = []
        all_dates = historical_calendar[historical_calendar['Trading Day'] == True].index
        
        for year in range(2008, 2026):
            for week in range(1, 54):
                week_days = [d for d in all_dates if d.isocalendar()[0] == year and d.isocalendar()[1] == week]
                if week_days:
                    weekly_last_trading_days.append(week_days[-1])
        
        return [d.strftime('%Y-%m-%d') for d in weekly_last_trading_days]

    def calculate_weekly_bollinger(df, length, std):
        """Calculate bollinger indicator using pandas_ta"""
        bb = ta.bbands(close=df['Close'], length=length, std=std)
        bb['Close'] = df['Close']
        return bb

    def analyze_weekly_bollinger_stocks(manual_date_dt, length, std, ticker_list, weekly_dates):
        start_date = start_d
        bollinger_filter = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        last_df = None

        for i, ticker in enumerate(ticker_list):
            try:
                status_text.text(f'Analyzing {ticker} (bollinger)... ({i+1}/{len(ticker_list)})')
                progress_bar.progress((i + 1) / len(ticker_list))
                try:
                    df = yf.download(ticker, start_date, manual_date_dt, interval="1d", progress=False)
                    time.sleep(0.1)
            
                    df.columns = df.columns.droplevel(1)
                    weekly_dates_idx = pd.to_datetime(weekly_dates)
                    week_end_df = df.loc[df.index.intersection(weekly_dates_idx)]
                    last_df = calculate_weekly_bollinger(week_end_df.copy(), length, std)

                    column_name = f'BBL_{length}_{float(std):.1f}'
                    if (last_df['Close'][-2] < last_df[column_name][-2]) and (last_df['Close'][-1] > last_df[column_name][-1]):
                        bollinger_filter.append(ticker)
                    else:
                        continue
                except:
                    continue
            except:
                continue

        return bollinger_filter
        
    if st.button('Run Weekly Bollinger Analysis'): 
        historical_calendar = create_historical_calendar()
        weekly_dates = get_weekly_dates(historical_calendar)

        bollinger_stocks = analyze_weekly_bollinger_stocks(manual_date, length, std, ticker_list, weekly_dates)
        st.write(bollinger_stocks)

        if bollinger_stocks:
            st.subheader("🎯 Bollinger Filtered Symbols")
            st.markdown("Stock list (one per line):")
            st.code("\n".join(bollinger_stocks))
            st.download_button(
                label="Download Bollinger Filtered Symbols (CSV)",
                data="\n".join(bollinger_stocks),
                file_name="weekly_bollinger_filtered_symbols.csv",
                mime="text/csv"
            )
        else:
            st.warning("⚠️ No stocks passed the weekly bollinger filter criteria")

elif selected_analysis == "Daily Supertrend":
    st.markdown("---")
    st.markdown("## 📅 Daily Supertrend Analysis Dashboard")
    st.markdown("*Apply supertrend filters using daily data (most recent trading day)*")
    
    # Supertrend Analysis Parameters
    st.subheader("🔧 Supertrend Parameters")
    col1, col2, col3 = st.columns(3)
    with col1:
        supertrend_period = st.number_input("Supertrend Period", min_value=1, max_value=50, value=10, key="daily_supertrend_period")
    with col2:
        supertrend_multiplier = st.number_input("Supertrend Multiplier", min_value=0.1, max_value=10.0, value=3.0, step=0.1, key="daily_supertrend_multiplier")

    def calculate_supertrend(df, period, multiplier):
        """Calculate Supertrend indicator using pandas_ta"""
        df.ta.supertrend(length=period, multiplier=multiplier, append=True, column="close")
        return df

    def analyze_supertrend_stocks(manual_date_dt, period, multiplier, ticker_list):
        start_date = start_d
        supertrend_filter = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        last_df = None

        for i, ticker in enumerate(ticker_list):
            try:
                status_text.text(f'Analyzing {ticker} (Supertrend)... ({i+1}/{len(ticker_list)})')
                progress_bar.progress((i + 1) / len(ticker_list))

                try:
                    df = yf.download(ticker, start_date, manual_date_dt, interval="1d", progress=False)
                    time.sleep(0.1)
            
                    if df.empty:
                        continue
                    df.columns = df.columns.droplevel(1)
                    
                    last_df = calculate_supertrend(df, period, multiplier)
                except:
                    continue
                
                column_name = f'SUPERTd_{period}_{float(multiplier):.1f}'
                if last_df[column_name].iloc[-1] > last_df[column_name][-2]: 
                    supertrend_filter.append(ticker)
                else:
                    continue
            except:
                continue

        return supertrend_filter
        
    if st.button('Run Daily Supertrend Analysis'): 
        supertrend_stocks = analyze_supertrend_stocks(manual_date, supertrend_period, supertrend_multiplier, ticker_list)
        st.write(supertrend_stocks)

        if supertrend_stocks:
            st.subheader("🎯 Supertrend Filtered Symbols")
            st.markdown("Stock list (one per line):")
            st.code("\n".join(supertrend_stocks))
            st.download_button(
                label="Download Supertrend Filtered Symbols (CSV)",
                data="\n".join(supertrend_stocks),
                file_name="daily_supertrend_filtered_symbols.csv",
                mime="text/csv"
            )
        else:
            st.warning("⚠️ No stocks passed the daily supertrend filter criteria")

elif selected_analysis == "Weekly Supertrend":
    st.markdown("---")
    st.markdown("## 📅 Weekly Supertrend Analysis Dashboard")
    st.markdown("*Apply supertrend filters using weekly data*")
    
    # Supertrend Analysis Parameters
    st.subheader("🔧 Supertrend Parameters")
    col1, col2, col3 = st.columns(3)
    with col1:
        supertrend_period = st.number_input("Supertrend Period", min_value=1, max_value=50, value=10, key="weekly_supertrend_period")
    with col2:
        supertrend_multiplier = st.number_input("Supertrend Multiplier", min_value=0.1, max_value=10.0, value=3.0, step=0.1, key="weekly_supertrend_multiplier")

    def calculate_supertrend(df, period, multiplier):
        """Calculate Supertrend indicator using pandas_ta"""
        df.ta.supertrend(length=period, multiplier=multiplier, append=True, column="close")
        return df

    def analyze_supertrend_stocks(manual_date_dt, period, multiplier, ticker_list):
        start_date = start_d
        supertrend_filter = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        last_df = None

        for i, ticker in enumerate(ticker_list):
            try:
                start_date = "2023-01-01"
                status_text.text(f'Analyzing {ticker} (Supertrend)... ({i+1}/{len(ticker_list)})')
                progress_bar.progress((i + 1) / len(ticker_list))
                try:
                    df = yf.download(ticker, start_date, manual_date_dt, interval="1wk", progress=False)
                    time.sleep(0.1)
             
                    df.columns = df.columns.droplevel(1)
                    if datetime.now().weekday() in [4,5,6]:
                        df1 = df
                    else:
                        df1 = df[:-1]
           
                    last_df = calculate_supertrend(df1.copy(), period, multiplier)
                    column_name = f'SUPERTd_{period}_{float(multiplier):.1f}'
                    if last_df[column_name].iloc[-1] > last_df[column_name][-2]: 
                        supertrend_filter.append(ticker)
                except:
                    continue
            except:
                continue

        return supertrend_filter
        
    if st.button('Run Weekly Supertrend Analysis'): 
        supertrend_stocks = analyze_supertrend_stocks(manual_date, supertrend_period, supertrend_multiplier, ticker_list)
        st.write(supertrend_stocks)

        if supertrend_stocks:
            st.subheader("🎯 Supertrend Filtered Symbols")
            st.markdown("Stock list (one per line):")
            st.code("\n".join(supertrend_stocks))
            st.download_button(
                label="Download Supertrend Filtered Symbols (CSV)",
                data="\n".join(supertrend_stocks),
                file_name="weekly_supertrend_filtered_symbols.csv",
                mime="text/csv"
            )
        else:
            st.warning("⚠️ No stocks passed the weekly supertrend filter criteria")

elif selected_analysis == "Daily Linear Regression":
    st.markdown("---")
    st.markdown("## 📅 Daily Regression Analysis Dashboard")
    st.markdown("*Apply regression filters using daily data (most recent trading day)*")
    
    # Regression Analysis Parameters
    st.subheader("🔧 Regression Parameters")
    col1, col2, col3 = st.columns(3)
    with col1:
        length = st.number_input("Regression Period", min_value=1, max_value=500, value=100, key="daily_regression_period")
    with col2:
        std = st.number_input("Regression Multiplier", min_value=0.1, max_value=10.0, value=2.0, step=0.1, key="daily_regression_multiplier")

    def calculate_regression(df, length=100, std=2):
        """Reproduces TradingView's 'Linear Regression Channel' indicator."""
        linreg_lines = []
        upper_band = []
        lower_band = []
        pearson_r_list = []

        for i in range(len(df)):
            if i < length - 1:
                linreg_lines.append(np.nan)
                upper_band.append(np.nan)
                lower_band.append(np.nan)
                pearson_r_list.append(np.nan)
            else:
                y = df['Close'].iloc[i - length + 1:i + 1].values
                x = np.arange(length)
                x_mean = x.mean()
                y_mean = y.mean()

                # Slope (m) and intercept (c)
                m = np.sum((x - x_mean) * (y - y_mean)) / np.sum((x - x_mean) ** 2)
                c = y_mean - m * x_mean

                # Linear regression line over the window
                linreg = m * x + c

                # Standard deviation of residuals
                residuals = y - linreg
                stddev = np.std(residuals)

                # Pearson's R
                numerator = np.sum((x - x_mean) * (y - y_mean))
                denominator = np.sqrt(np.sum((x - x_mean) ** 2) * np.sum((y - y_mean) ** 2))
                pearson_r = numerator / denominator if denominator != 0 else 0

                # Add value at the latest point
                linreg_lines.append(linreg[-1])
                upper_band.append(linreg[-1] + std * stddev)
                lower_band.append(linreg[-1] - std * stddev)
                pearson_r_list.append(pearson_r)

        df['linreg'] = linreg_lines
        df['upper'] = upper_band
        df['lower'] = lower_band
        df['pearson_r'] = pearson_r_list

        return df

    def analyze_regression_stocks(manual_date_dt, length, std, ticker_list):
        start_date = start_d
        regression_filter = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        last_df = None

        for i, ticker in enumerate(ticker_list):
            try:
                status_text.text(f'Analyzing {ticker} (regression)... ({i+1}/{len(ticker_list)})')
                progress_bar.progress((i + 1) / len(ticker_list))

                try:
                    df = yf.download(ticker, start_date, manual_date_dt, interval="1d", progress=False)
                    time.sleep(0.1)
                    
                    if df.empty:
                        continue
                    df.columns = df.columns.droplevel(1)
                    
                    last_df = calculate_regression(df, length, std)
                except:
                    continue
                
                if (last_df['Close'][-2] < last_df['lower'][-2]) and (last_df['Close'][-1] > last_df['lower'][-1]):
                    regression_filter.append(ticker)
                else:
                    continue
            except:
                continue

        return regression_filter
        
    if st.button('Run Daily Regression Analysis'): 
        regression_stocks = analyze_regression_stocks(manual_date, length, std, ticker_list)
        st.write(regression_stocks)

        if regression_stocks:
            st.subheader("🎯 Regression Filtered Symbols")
            st.markdown("Stock list (one per line):")
            st.code("\n".join(regression_stocks))
            st.download_button(
                label="Download Regression Filtered Symbols (CSV)",
                data="\n".join(regression_stocks),
                file_name="daily_regression_filtered_symbols.csv",
                mime="text/csv"
            )
        else:
            st.warning("⚠️ No stocks passed the daily regression filter criteria")

elif selected_analysis == "Weekly Linear Regression":
    st.markdown("---")
    st.markdown("## 📅 Weekly Regression Analysis Dashboard")
    st.markdown("*Apply regression filters using weekly data*")
    
    # Regression Analysis Parameters
    st.subheader("🔧 Regression Parameters")
    col1, col2, col3 = st.columns(3)
    with col1:
        length = st.number_input("Regression Period", min_value=1, max_value=500, value=100, key="weekly_regression_period")
    with col2:
        std = st.number_input("Regression Multiplier", min_value=0.1, max_value=10.0, value=2.0, step=0.1, key="weekly_regression_multiplier")

    def get_weekly_dates(historical_calendar):
        """Get weekly last trading dates"""
        weekly_last_trading_days = []
        all_dates = historical_calendar[historical_calendar['Trading Day'] == True].index
        
        for year in range(2008, 2026):
            for week in range(1, 54):
                week_days = [d for d in all_dates if d.isocalendar()[0] == year and d.isocalendar()[1] == week]
                if week_days:
                    weekly_last_trading_days.append(week_days[-1])
        
        return [d.strftime('%Y-%m-%d') for d in weekly_last_trading_days]

    def calculate_regression(df, length=100, std=2):
        """Reproduces TradingView's 'Linear Regression Channel' indicator."""
        linreg_lines = []
        upper_band = []
        lower_band = []
        pearson_r_list = []

        for i in range(len(df)):
            if i < length - 1:
                linreg_lines.append(np.nan)
                upper_band.append(np.nan)
                lower_band.append(np.nan)
                pearson_r_list.append(np.nan)
            else:
                y = df['Close'].iloc[i - length + 1:i + 1].values
                x = np.arange(length)
                x_mean = x.mean()
                y_mean = y.mean()

                # Slope (m) and intercept (c)
                m = np.sum((x - x_mean) * (y - y_mean)) / np.sum((x - x_mean) ** 2)
                c = y_mean - m * x_mean

                # Linear regression line over the window
                linreg = m * x + c

                # Standard deviation of residuals
                residuals = y - linreg
                stddev = np.std(residuals)

                # Pearson's R
                numerator = np.sum((x - x_mean) * (y - y_mean))
                denominator = np.sqrt(np.sum((x - x_mean) ** 2) * np.sum((y - y_mean) ** 2))
                pearson_r = numerator / denominator if denominator != 0 else 0

                # Add value at the latest point
                linreg_lines.append(linreg[-1])
                upper_band.append(linreg[-1] + std * stddev)
                lower_band.append(linreg[-1] - std * stddev)
                pearson_r_list.append(pearson_r)

        df['linreg'] = linreg_lines
        df['upper'] = upper_band
        df['lower'] = lower_band
        df['pearson_r'] = pearson_r_list

        return df

    def analyze_regression_stocks(manual_date_dt, length, std, ticker_list, weekly_dates):
        start_date = start_d
        regression_filter = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        last_df = None

        for i, ticker in enumerate(ticker_list):
            try:
                status_text.text(f'Analyzing {ticker} (regression)... ({i+1}/{len(ticker_list)})')
                progress_bar.progress((i + 1) / len(ticker_list))
                try:
                    df = yf.download(ticker, start_date, manual_date_dt, interval="1wk", progress=False)
                    time.sleep(0.1)
             
                    df.columns = df.columns.droplevel(1)
                    if datetime.now().weekday() in [4,5,6]:
                        df1 = df
                    else:
                        df1 = df[:-1]
           
                    last_df = calculate_regression(df1.copy(), length, std)

                    if (last_df['Close'][-2] < last_df['lower'][-2]) and (last_df['Close'][-1] > last_df['lower'][-1]):
                        regression_filter.append(ticker)
                    else:
                        continue
                except:
                    continue
            except:
                continue

        return regression_filter
        
    if st.button('Run Weekly Regression Analysis'): 
        historical_calendar = create_historical_calendar()
        weekly_dates = get_weekly_dates(historical_calendar)

        regression_stocks = analyze_regression_stocks(manual_date, length, std, ticker_list, weekly_dates)
        st.write(regression_stocks)

        if regression_stocks:
            st.subheader("🎯 Regression Filtered Symbols")
            st.markdown("Stock list (one per line):")
            st.code("\n".join(regression_stocks))
            st.download_button(
                label="Download Regression Filtered Symbols (CSV)",
                data="\n".join(regression_stocks),
                file_name="weekly_regression_filtered_symbols.csv",
                mime="text/csv"
            )
        else:
            st.warning("⚠️ No stocks passed the weekly regression filter criteria")

else:
    st.info("👆 Please select an analysis type from the dropdown menu above to get started!")


"""Configuration and constants for vault generation."""
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VAULT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
JSON_FILE = os.path.join(VAULT_ROOT, 'data', 'sih2026_problem_statements.json')
SOURCE_URL = 'https://www.sih.gov.in/sih2026PS'

DIRS = {
    'meta': '00-Meta',
    'ps': '01-Problem-Statements',
    'themes': '02-Themes',
    'orgs': '03-Organizations',
    'tech': '04-Technologies',
    'domains': '05-Domains',
    'indexes': '06-Indexes',
}

TECH_KEYWORDS = {
    'AI-and-ML': [r'\bAI\b', r'\bML\b', r'artificial intelligence', r'machine learning', r'deep learning', r'neural network', r'Al-Based', r'Al-Powered', r'Al-Driven', r'AI-Based', r'AI-Powered', r'AI-Driven', r'Al-Enabled', r'AI-Enabled'],
    'Computer-Vision': [r'computer vision', r'image processing', r'object detection', r'image recognition', r'image analysis', r'visual perception', r'fundus', r'retinal'],
    'NLP': [r'\bNLP\b', r'natural language', r'text mining', r'language model', r'\bLLM\b', r'chatbot', r'text analysis', r'multilingual', r'RAG-based'],
    'IoT-and-Sensors': [r'\bIoT\b', r'internet of things', r'\bsensor\b', r'\bsensors\b', r'embedded system', r'wearable'],
    'Blockchain': [r'blockchain', r'distributed ledger', r'smart contract', r'cryptocurrency', r'crypto'],
    'GIS-and-Geospatial': [r'\bGIS\b', r'geospatial', r'satellite imagery', r'remote sensing', r'mapping', r'cadastral', r'geo-coded', r'geo-tagged'],
    'Robotics': [r'robot', r'rover', r'drone', r'\bUAV\b', r'\bAMR\b', r'quadruped'],
    'Cloud-Computing': [r'cloud', r'\bSaaS\b', r'microservice', r'cloud-based'],
    'Mobile-Development': [r'mobile app', r'android', r'\biOS\b', r'mobile.based', r'mobile application'],
    'Web-Platforms': [r'web.based', r'web platform', r'\bportal\b', r'dashboard', r'web application'],
    'Data-Analytics': [r'data analytics', r'big data', r'predictive analytics', r'data mining', r'data visualization'],
    'Cybersecurity-Tech': [r'cyber', r'encryption', r'forensic', r'malware', r'threat detection', r'intrusion', r'penetration'],
    'AR-VR': [r'\bAR\b.*reality', r'\bVR\b', r'augmented reality', r'virtual reality'],
    'Digital-Twin': [r'digital twin'],
    'Edge-Computing': [r'edge.?AI', r'edge computing', r'on.?device', r'on-device'],
    'LiDAR': [r'\blidar\b', r'\bLiDAR\b'],
    'Quantum-Computing': [r'quantum'],
    'GPS-and-Navigation': [r'\bGPS\b', r'navigation system', r'\bGNSS\b', r'dead reckoning'],
    '3D-Modeling': [r'\b3D\b', r'three.dimensional', r'point cloud', r'3D model'],
    'Sonar-Acoustics': [r'\bsonar\b', r'acoustic', r'side.scan'],
}

DOMAIN_KEYWORDS = {
    'Healthcare': [r'health', r'medical', r'clinical', r'patient', r'disease', r'hospital', r'diagnosis', r'retinopathy', r'dementia', r'mastitis'],
    'Agriculture': [r'agricultur', r'farm', r'crop', r'dairy', r'livestock', r'irrigation', r'soil', r'beekeep', r'honey', r'silage', r'feed quality'],
    'Mining': [r'\bmine\b', r'\bmining\b', r'\bcoal\b', r'\bore\b', r'\bmineral\b', r'manganese', r'subsidence'],
    'Defence-and-Military': [r'defence', r'defense', r'military', r'army', r'artillery', r'weapon', r'\bDRDO\b', r'tactical', r'anti.drone', r'ammunition', r'fuze'],
    'Land-Management': [r'land record', r'cadastral', r'land acquisition', r'\bULPIN\b', r'land governance', r'parcel mapping'],
    'Weather-and-Climate': [r'weather', r'meteorolog', r'rainfall', r'cyclone', r'monsoon', r'forecast', r'climate', r'thunderstorm', r'heatwave', r'nowcast'],
    'Ocean-and-Marine': [r'ocean', r'marine', r'underwater', r'seafloor', r'polar', r'antarctic', r'iceberg', r'sea.ice'],
    'Transportation': [r'railway', r'\btrain\b', r'traffic', r'logistics', r'freight', r'vehicle tracking'],
    'Education-and-Skilling': [r'education', r'learning platform', r'training', r'skill mapping', r'pedagogy', r'competency'],
    'Disaster-Response': [r'disaster', r'flood', r'landslide', r'earthquake', r'rescue', r'emergency', r'early warning', r'inundation'],
    'Law-Enforcement': [r'police', r'criminal', r'forensic', r'surveillance', r'border', r'law enforcement', r'narcotics', r'NCRB'],
    'Energy-and-Petroleum': [r'petroleum', r'oil well', r'crude oil', r'refinery', r'sucker rod', r'drilling'],
    'Urban-Development': [r'urban', r'smart city', r'municipal', r'urban flood', r'waste management'],
    'E-Governance': [r'governance', r'government scheme', r'compliance', r'procurement', r'\bGeM\b', r'MPLAD'],
    'Space-Exploration': [r'space station', r'satellite', r'\bISRO\b', r'chandrayaan', r'astronaut', r'BAS experiment'],
    'Social-Welfare': [r'cooperative', r'artisan', r'tribal', r'marginalized', r'SC communities', r'atrocities', r'welfare'],
}

ORG_TYPES = {
    'Government': ['Ministry', 'AICTE', 'DRDO', 'ISRO', 'MoSPI', 'Government', 'Governmcnt', 'All India Council', 'NTRO'],
    'Industry': ['MathWorks', 'Autodesk', 'Qualcomm', 'Egreen', 'Bharat Electronics'],
    'PSU': ['Oil India', 'NMDC', 'Mangalore Refinery', 'MRPL'],
}

def classify_org_type(org_name):
    for otype, keywords in ORG_TYPES.items():
        if any(k in org_name for k in keywords):
            return otype
    return 'Other'

def sanitize_filename(name):
    """Convert a name to a safe, clean filename."""
    import re
    name = re.sub(r'[()<>:"/\\|?*]', '', name)
    name = re.sub(r'[\s&]+', '-', name)
    name = re.sub(r'-+', '-', name)
    name = name.strip('-')
    return name


def rel_link(label, from_subdir, to_subdir, filename):
    """Generate a clean relative Markdown link between vault directories.
    If from_subdir is empty/None, relative path is from root (e.g. '01-Problem-Statements/PS-26001.md').
    If from_subdir is equal to to_subdir, relative path is './filename'.
    Otherwise, relative path is '../to_subdir/filename'.
    """
    if not filename.endswith('.md'):
        filename += '.md'
    if not from_subdir:
        path = f"{to_subdir}/{filename}"
    elif from_subdir == to_subdir:
        path = f"./{filename}"
    else:
        path = f"../{to_subdir}/{filename}"
    return f"[{label}]({path})"


import random
import pandas as pd
from sqlalchemy import create_engine
from faker import Faker

# 📌 הגדרות חיבור ל-PostgreSQL (וודא שהדוקר פועל)
DB_HOST = "localhost"  # אם לא עובד, נסי "host.docker.internal"
DB_PORT = "5432"
DB_NAME = "mydatabase"
DB_USER = "myuser"
DB_PASS = "mypassword"

# 🔗 יצירת חיבור למסד הנתונים
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# 📌 רשימת סוגי ההתנדבויות לעמותת עזר מציון
volunteer_types = [
    "Assistance to Holocaust survivors",
    "Visit to the sick",
    "Preparation of food packages",
    "Assistance to the elderly",
    "Preparation for Passover",
    "Support for victims of terrorism",
    "Assistance to children at risk",
    "Support centers for women",
    "Support for pregnant women",
    "Assistance in rehabilitation centers",
    "Providing transportation for medical appointments",
    "Organizing charity events for cancer patients",
    "Organizing support for families of fallen soldiers",
    "Offering emotional support to individuals with chronic illnesses",
    "Visiting hospitalized children",
    "Organizing medical equipment donations",
    "Assisting with mobility aids for the elderly",
    "Providing home care for the elderly",
    "Organizing health awareness workshops for the elderly",
    "Organizing group therapy sessions for cancer patients",
    "Home visits for elderly people living alone",
    "Providing care packages for people with disabilities",
    "Providing financial assistance for medical treatments",
    "Creating a buddy system for elderly citizens",
    "Organizing awareness events for mental health",
    "Offering respite care for family caregivers",
    "Assisting in emergency response teams during crises",
    "Coordinating volunteer drivers for medical transport",
    "Providing assistance to families with special needs children",
    "Organizing food drives for the needy",
    "Running blood donation campaigns",
    "Providing tutoring for children from low-income families",
    "Offering mental health support for people in crisis",
    "Providing food and clothing for families in need",
    "Visiting isolated elderly individuals",
    "Coordinating therapy programs for children with special needs",
    "Volunteering in daycare centers for at-risk children",
    "Organizing recreational activities for children in hospitals",
    "Organizing charity runs for medical causes",
    "Providing social support to families of cancer patients",
    "Running educational workshops for people with disabilities",
    "Volunteering in nursing homes for the elderly",
    "Providing emergency relief in natural disasters",
    "Organizing birthday celebrations for children in need",
    "Assisting in rehabilitating addicts",
    "Offering legal aid for underprivileged families",
    "Organizing job training programs for the unemployed",
    "Distributing medical supplies to underserved communities",
    "Offering grief counseling for families who have lost loved ones",
    "Organizing holiday camps for children in need",
    "Providing therapeutic services for those affected by trauma",
    "Supporting caregivers of individuals with disabilities",
    "Organizing family support groups",
    "Assisting with the integration of refugees into local communities",
    "Providing shelter for the homeless",
    "Running stress relief workshops for caregivers",
    "Organizing events for people with disabilities",
    "Assisting in providing transportation for medical emergencies",
    "Supporting veterans and their families",
    "Organizing creative workshops for patients in rehabilitation",
    "Offering phone support to elderly individuals living alone",
    "Organizing community cleaning projects",
    "Providing education on financial literacy for the needy",
    "Coordinating respite care for families with seriously ill members",
    "Offering support for parents of children with special needs",
    "Running social activities for children from at-risk communities",
    "Organizing book drives for underprivileged students",
    "Providing community-based mental health services",
    "Supporting projects for accessible housing for people with disabilities",
    "Organizing events to raise awareness for childhood illnesses",
    "Offering professional development workshops for unemployed individuals",
    "Organizing volunteering opportunities for young people",
    "Running nutritional support programs for low-income families",
    "Assisting people in need of legal advocacy services",
    "Offering guidance on parenting for families in crisis",
    "Providing recreational activities for elderly people in nursing homes",
    "Helping families with home-schooling resources",
    "Assisting with technology education for elderly individuals",
    "Organizing charity art shows to raise funds for medical research",
    "Coordinating tutoring programs for children with learning disabilities",
    "Organizing food distribution events for people affected by poverty",
    "Visiting hospitals to comfort patients undergoing treatments",
    "Running community empowerment programs for women",
    "Offering employment support for disabled individuals",
    "Organizing free medical check-ups for low-income communities",
    "Organizing winter coat drives for the needy",
    "Offering companionship to people living with dementia",
    "Coordinating child-friendly spaces for children in hospitals",
    "Running after-school programs for at-risk youth",
    "Organizing health education campaigns in underserved areas",
    "Offering career counseling for individuals facing unemployment",
    "Assisting in organizing funerals for families with limited resources",
    "Running support groups for caregivers of people with Alzheimer's",
    "Organizing charity dinners to fund medical treatments",
    "Supporting families of people in long-term care",
    "Assisting in providing mental health support for veterans",
    "Coordinating community outreach for cancer survivors",
    "Organizing medical missions for underserved communities",
    "Offering assistance to families during the High Holidays",
    "Helping with home repairs for elderly or disabled individuals",
    "Organizing community fundraising events for medical treatments",
    "Assisting with translation services for immigrant families",
    "Offering therapy dogs for emotional support",
    "Providing supplies for children’s hospitals",
    "Assisting with post-operative recovery at home",
    "Organizing charity concerts to raise funds for medical causes",
    "Supporting organizations that help victims of domestic violence",
    "Providing free legal clinics for people in need",
    "Organizing community dinners for people in need",
    "Assisting in developing self-care programs for caregivers",
    "Running youth empowerment initiatives",
    "Supporting children with chronic illnesses",
    "Providing assistance for the homeless during winter",
    "Organizing sports and fitness programs for children at risk",
    "Assisting families affected by fire or other disasters",
    "Organizing cultural events for the elderly",
    "Providing personal hygiene products for the homeless",
    "Visiting hospitals to offer emotional support to families",
    "Helping with the logistics of medical supply donations",
    "Offering support to caregivers of people with terminal illnesses",
    "Organizing health and wellness programs for cancer patients",
    "Running meal prep services for families with ill members",
    "Providing safe spaces for women affected by domestic violence",
    "Organizing holiday parties for children in hospitals",
    "Providing companionship to individuals with severe disabilities",
    "Assisting with medical transportation for elderly individuals",
    "Coordinating volunteer caregivers for individuals with disabilities",
    "Organizing grief support workshops for families of terminally ill",
    "Providing temporary housing for families in crisis",
    "Helping low-income families access medical insurance",
    "Providing support to refugees adjusting to life in Israel",
    "Organizing yoga and relaxation sessions for cancer patients",
    "Coordinating home visits for elderly people in nursing homes",
    "Running creative workshops for patients in rehabilitation centers",
    "Organizing and distributing books to children in need",
    "Helping organize food kitchens for the homeless",
    "Assisting in the management of community outreach programs",
    "Providing emotional support for individuals in palliative care",
    "Running social media campaigns for medical causes",
    "Helping individuals transition from hospital to home care",
    "Supporting religious and spiritual needs of patients",
    "Running workshops on coping with chronic illness",
    "Providing administrative support for healthcare workers",
    "Organizing knitting and crochet programs for children in need",
    "Offering support groups for individuals with disabilities",
    "Helping with transportation for seniors to social activities",
    "Organizing toy drives for children in hospitals",
    "Supporting efforts to improve public health awareness",
    "Helping with translation for medical appointments",
    "Assisting with managing chronic health conditions",
    "Organizing volunteer cleaning teams for public spaces",
    "Running blood drives to support hospitals",
    "Organizing community-based health screenings",
    "Helping organize disaster relief efforts",
    "Providing social interaction for elderly individuals in care homes",
    "Running meditation and mindfulness sessions for patients",
    "Organizing free workshops on self-care for caregivers",
    "Providing meals and snacks for families in hospital waiting rooms",
    "Offering hands-on help with daily living for individuals with disabilities",
    "Assisting in coordinating volunteers for fundraising events",
    "Running programs to help children in hospitals stay connected with their peers",
    "Providing home schooling for children with illnesses",
    "Organizing awareness days for rare diseases",
    "Helping elderly people with grocery shopping",
    "Providing assistance to families of fallen soldiers",
    "Organizing mentorship programs for children with chronic illness",
    "Running programs for children of incarcerated parents",
    "Helping the elderly with home maintenance tasks",
    "Providing after-school programs for children from low-income families",
    "Running programs to support widows and widowers",
    "Providing dental care services for underserved populations",
    "Coordinating community drives for used clothing and goods",
    "Providing wheelchair access and support for the elderly",
    "Assisting children with special needs in hospitals",
    "Helping to organize charity fashion shows to raise awareness",
    "Providing emotional support for individuals recovering from trauma"
]

# 🔗 שליפת רשימת המתנדבים הפעילים מהטבלה Volunteer
volunteers_query = "SELECT volunteer_id FROM Volunteer;"
volunteers_df = pd.read_sql(volunteers_query, engine)

# 📌 יצירת רשימת נתונים לשם הוספה לטבלה
kind_of_vol_data = []
kind_of_vol_id = 1  # אתחול של ה-ID הראשון

for volunteer_type in volunteer_types:
    volunteer_id = random.choice(volunteers_df['volunteer_id'].tolist())

    kind_of_vol_data.append({
        "kindofvol_id": kind_of_vol_id,
        "type": volunteer_type,
        "volunteer_id": volunteer_id
    })

    kind_of_vol_id += 1  # העלאת ה-ID כדי לשמור על סדר

# 📌 יצירת DataFrame ושמירה למסד הנתונים
kind_of_vol_df = pd.DataFrame(kind_of_vol_data)

# 📌 הוספת הנתונים לטבלה PostgreSQL
kind_of_vol_df.to_sql('kindofvol', engine, if_exists='append', index=False, schema='public')

print("✅ סוגי ההתנדבויות הוזנו בהצלחה לטבלה 'KindOfVol'!")

import random
import pandas as pd
from sqlalchemy import create_engine
from faker import Faker

# 📌 הגדרות חיבור ל-PostgreSQL (וודאי שהדוקר פועל)
DB_HOST = "localhost"  # אם לא עובד, נסי "host.docker.internal"
DB_PORT = "5432"
DB_NAME = "mydatabase"
DB_USER = "myuser"
DB_PASS = "mypassword"

# 🔗 יצירת חיבור למסד הנתונים
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# 🔍 שליפת רשימת הערים מהטבלה City
cities_query = "SELECT name FROM City;"
cities_df = pd.read_sql(cities_query, engine)

# 🔍 שליפת רשימת המתנדבים הפעילים מהטבלה Volunteer
volunteers_query = "SELECT volunteer_id FROM Volunteer;"
volunteers_df = pd.read_sql(volunteers_query, engine)

# 📌 רשימת שמות של אירועים למתנדבים
event_names = [
    "Volunteer Appreciation Dinner", "Leadership Training for Volunteers",
    "Personal Development Workshop", "Team Building Activity for Volunteers",
    "Motivational Speech Event", "Creative Writing Workshop for Volunteers",
    "Health and Wellness for Volunteers", "Mindfulness and Stress Relief Session",
    "Volunteer Networking Mixer", "First Aid Training for Volunteers",
    "Community Volunteer Meet-up", "DIY Crafting Workshop for Volunteers",
    "Time Management Skills for Volunteers", "Volunteer Empowerment Workshop",
    "Public Speaking Skills for Volunteers", "Conflict Resolution Training for Volunteers",
    "Volunteer Photography Workshop", "Social Media Skills for Volunteers",
    "Fundraising Event Planning for Volunteers", "Volunteer Yoga and Meditation",
    "Crisis Management for Volunteers", "Volunteer Leadership Retreat",
    "Team Collaboration Skills for Volunteers", "Volunteer Adventure Day",
    "Creative Problem Solving for Volunteers", "Team Building Adventure for Volunteers",
    "Nonprofit Marketing for Volunteers", "Volunteer Talent Show",
    "Volunteer Appreciation Picnic", "Stress Management Workshop for Volunteers",
    "Networking Event for Nonprofit Volunteers", "Event Planning Workshop for Volunteers",
    "Digital Skills Training for Volunteers", "Volunteer Management Skills Workshop",
    "Volunteer Diversity and Inclusion Training", "Nonprofit Strategy and Leadership for Volunteers",
    "Volunteering for Social Change", "Volunteer Retreat and Relaxation Day",
    "Volunteer Skills Enhancement Workshop", "Public Relations Skills for Volunteers",
    "Building Emotional Intelligence for Volunteers", "Volunteer Mentorship Program",
    "Volunteer Recognition Ceremony", "Social Impact and Volunteerism Conference",
    "Creative Workshop for Volunteers", "Health and Nutrition for Volunteers",
    "Volunteer Communication Skills Training", "Personal Branding for Volunteers",
    "Digital Storytelling for Volunteers", "Volunteer Career Development Session",
    "Networking and Career Building for Volunteers", "Volunteer Appreciation Day",
    "Volunteer Leadership Forum", "Mindset and Motivation for Volunteers",
    "Volunteer Project Management Training", "Interactive Art Workshop for Volunteers",
    "Volunteer Fundraising Campaign Training", "Green Volunteerism and Sustainability",
    "Volunteer Career Coaching Session", "Stress Relief and Resilience Training for Volunteers",
    "Teamwork and Collaboration for Volunteers", "Empowering Women Volunteers Workshop",
    "Volunteer Engagement and Retention Strategies", "Volunteer Storytelling and Advocacy",
    "Fundraising for Nonprofits Workshop", "Volunteer Work-Life Balance Training",
    "Volunteer Training for Mentors", "Community Service Leadership Program",
    "Volunteer-Driven Innovation Session", "Resilience and Adaptability Training for Volunteers",
    "Advanced Communication Skills for Volunteers", "Volunteer Talent Development Program",
    "Leadership Development for Young Volunteers", "Digital Volunteerism and Social Impact",
    "Volunteer Creative Problem-Solving Workshop", "Volunteers Supporting Volunteers – Peer Training",
    "Nonprofit Operations and Leadership Workshop", "Public Speaking Masterclass for Volunteers",
    "Stress-Free Volunteering Tips and Tricks", "Volunteer Mindfulness Retreat",
    "Teamwork and Conflict Management for Volunteers", "Volunteer Networking Brunch",
    "Volunteer Storytelling for Social Change", "Leadership and Emotional Intelligence for Volunteers",
    "Volunteer Business Skills for Nonprofit Success", "Building a Volunteer-Friendly Organization",
    "Introduction to Project Management for Volunteers", "Volunteer Safety and Crisis Management Training",
    "Volunteer Empowerment Through Education", "Volunteer Writing for Advocacy and Change",
    "Public Speaking for Advocacy and Nonprofits", "Empowering Volunteers Through Knowledge Sharing",
    "Volunteers Making a Difference Event", "Transforming Communities Through Volunteering",
    "Volunteer Innovations in Social Responsibility", "Developing Volunteer Skills for Career Growth",
    "Volunteer Engagement Through Digital Platforms", "Nonprofit Event Planning for Volunteers",
    "Building an Inclusive Volunteer Program", "Volunteer Feedback and Growth Session"
]

# 🎉 יצירת 400 אירועים שונים
fake = Faker()
num_events = 400
events_data = []

for _ in range(num_events):
    event_name = random.choice(event_names)
    city_name = random.choice(cities_df['name'].tolist())
    manager_id = random.choice(volunteers_df['volunteer_id'].tolist())
    event_date = fake.date_between(start_date="-1y", end_date="today")

    events_data.append({
        "event_name": event_name,
        "event_date": event_date,
        "city_name": city_name,
        "manager_id": manager_id
    })

# 📌 יצירת DataFrame ושמירה לקובץ CSV
events_df = pd.DataFrame(events_data)
events_df.to_csv("mock_volunteer_events_400.csv", index=False)

print("✅ קובץ mock_volunteer_events_400.csv נוצר בהצלחה!")
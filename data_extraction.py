import requests
from bs4 import BeautifulSoup
import pandas as pd

# Initialize an empty list to store all course data
all_courses = []

# Loop through all 9 pages
for page_num in range(1, 10):
    url = f"https://courses.analyticsvidhya.com/collections/courses?page={page_num}"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        course_cards = soup.find_all('a', class_='course-card')

        for card in course_cards:
            heading = card.find('h3').text.strip() if card.find('h3') else None
            lessons = card.find('span', class_='course-card__lesson-count')
            lesson_count = lessons.text.strip() if lessons else None

            rating_section = card.find('div', class_='course-card__reviews')
            if rating_section:
                stars = rating_section.find_all('i', class_='fa-star')
                rating = len(stars)
                rating_count = rating_section.find('span', class_='review__stars-count')
                rating_count = rating_count.text.strip('()') if rating_count else None
            else:
                rating = None
                rating_count = None

            # Capture the direct course URL
            course_url = card['href'] if 'href' in card.attrs else None
            full_course_url = f"https://courses.analyticsvidhya.com{course_url}" if course_url else None

            all_courses.append({
                'Course Heading': heading,
                'Number of Lessons': lesson_count,
                'Rating': rating,
                'Number of Ratings': rating_count,
                'Course URL': full_course_url
            })
        print(f"Page {page_num} scraped successfully!")
    else:
        print(f"Failed to fetch page {page_num}. Status code: {response.status_code}")

# Save all the data into an Excel file
df = pd.DataFrame(all_courses)
df.to_excel('all_courses_analyticsvidhya.xlsx', index=False)
print("Data from all pages saved to 'all_courses_analyticsvidhya.xlsx'")

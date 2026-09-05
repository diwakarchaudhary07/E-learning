from django.core.management.base import BaseCommand

from studybee.models import Course


COURSES = [
    {
        'title': 'Python Programming Foundations',
        'category': 'Computer Science',
        'instructor': 'Aarav Mehta',
        'description': 'Build a strong programming foundation with Python, problem solving, and practical coding projects.',
        'price': 4999,
        'discount_price': 2999,
        'language': 'English',
        'duration': '8 weeks',
        'total_lessons': 32,
        'total_quizzes': 8,
    },
    {
        'title': 'Full Stack Web Development',
        'category': 'Computer Science',
        'instructor': 'Neha Kapoor',
        'description': 'Learn HTML, CSS, JavaScript, Django, databases, and deployment by building a complete web application.',
        'price': 7999,
        'discount_price': 4999,
        'language': 'English',
        'duration': '12 weeks',
        'total_lessons': 48,
        'total_quizzes': 12,
    },
    {
        'title': 'Data Science with Python',
        'category': 'Computer Science',
        'instructor': 'Rohan Verma',
        'description': 'Explore data analysis, visualization, and machine learning with Python and real-world datasets.',
        'price': 8999,
        'discount_price': 5499,
        'language': 'English',
        'duration': '14 weeks',
        'total_lessons': 56,
        'total_quizzes': 14,
    },
    {
        'title': 'Business Management Essentials',
        'category': 'Management',
        'instructor': 'Priya Shah',
        'description': 'Understand planning, decision-making, operations, and the core skills needed to manage a business.',
        'price': 5999,
        'discount_price': 3499,
        'language': 'English',
        'duration': '8 weeks',
        'total_lessons': 30,
        'total_quizzes': 8,
    },
    {
        'title': 'Digital Marketing Strategy',
        'category': 'Management',
        'instructor': 'Kabir Malhotra',
        'description': 'Create practical marketing campaigns using SEO, social media, content, email, and performance analytics.',
        'price': 4999,
        'discount_price': 2799,
        'language': 'English',
        'duration': '6 weeks',
        'total_lessons': 24,
        'total_quizzes': 6,
    },
    {
        'title': 'Leadership and Team Building',
        'category': 'Management',
        'instructor': 'Ananya Rao',
        'description': 'Develop communication, leadership, conflict resolution, and team-building skills for the modern workplace.',
        'price': 4499,
        'discount_price': 2499,
        'language': 'English',
        'duration': '5 weeks',
        'total_lessons': 20,
        'total_quizzes': 5,
    },
    {
        'title': 'Modern Sustainable Agriculture',
        'category': 'Agriculture',
        'instructor': 'Dr. Meera Joshi',
        'description': 'Learn sustainable farming methods, soil health, water management, and climate-smart agriculture practices.',
        'price': 3999,
        'discount_price': 2299,
        'language': 'English',
        'duration': '7 weeks',
        'total_lessons': 28,
        'total_quizzes': 7,
    },
    {
        'title': 'Organic Farming and Soil Management',
        'category': 'Agriculture',
        'instructor': 'Vikram Singh',
        'description': 'Discover organic inputs, crop rotation, composting, pest control, and healthy soil management.',
        'price': 3499,
        'discount_price': 1999,
        'language': 'English',
        'duration': '6 weeks',
        'total_lessons': 24,
        'total_quizzes': 6,
    },
    {
        'title': 'Agribusiness and Farm Entrepreneurship',
        'category': 'Agriculture',
        'instructor': 'Nisha Patel',
        'description': 'Turn agricultural ideas into viable businesses through planning, market research, finance, and supply chains.',
        'price': 4999,
        'discount_price': 2999,
        'language': 'English',
        'duration': '8 weeks',
        'total_lessons': 32,
        'total_quizzes': 8,
    },
    {
        'title': 'Introduction to Indian Law',
        'category': 'Law',
        'instructor': 'Adv. Sameer Khan',
        'description': 'Get an accessible overview of legal systems, constitutional principles, rights, duties, and courts in India.',
        'price': 5999,
        'discount_price': 3499,
        'language': 'English',
        'duration': '8 weeks',
        'total_lessons': 32,
        'total_quizzes': 8,
    },
    {
        'title': 'Business and Contract Law',
        'category': 'Law',
        'instructor': 'Adv. Kavita Iyer',
        'description': 'Learn the essentials of contracts, business obligations, negotiation, remedies, and commercial risk.',
        'price': 6499,
        'discount_price': 3899,
        'language': 'English',
        'duration': '9 weeks',
        'total_lessons': 36,
        'total_quizzes': 9,
    },
    {
        'title': 'Cyber Law and Digital Rights',
        'category': 'Law',
        'instructor': 'Adv. Arjun Menon',
        'description': 'Understand cyber offences, privacy, online agreements, intellectual property, and digital rights.',
        'price': 5499,
        'discount_price': 3199,
        'language': 'English',
        'duration': '7 weeks',
        'total_lessons': 28,
        'total_quizzes': 7,
    },
]


class Command(BaseCommand):
    help = 'Create or update demo courses across the main learning branches.'

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        for course_data in COURSES:
            _, created = Course.objects.update_or_create(
                title=course_data['title'],
                defaults=course_data,
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Demo course catalog ready: {created_count} created, {updated_count} updated.'
            )
        )

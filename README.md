# St Jude School - Student's Government Election System

<p align="center">
  <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQik7ZJRLnYVzi5A9VZ2RSt0FT5QOH255c-vA&s" alt="Logo" width="100%" 
       style="border-radius: 70px";>
</p>


## About

The Student's Government Election System is a web-based application designed to facilitate secure and efficient student government elections at the School of St Jude. This project was initiated by Miss Elizabeth and developed in collaboration with PearlK Tech Humphrey and Christopher to modernize the voting process and encourage student participation in school democracy.

This project is a proud result of the partnership between **JR Institute of Information Technology** and **The School of St Jude** under their joint program for building Youth Capacity in Technology. The collaboration aims to empower young minds with practical tech skills while solving real-world challenges.



## Important Notice

This repository is maintained as a reference implementation. If you'd like to use or study this system:

1. Please **fork** the repository rather than cloning it directly
2. Use the forked version for your implementation
3. Respect the original attribution and partnership credits

## Features

- 🔐 Secure authentication system
- 📊 Real-time election results
- 👥 User role management (Admin, Student, Candidate)
- 🗳️ Multiple election support
- 📱 Responsive design
- 📈 Analytics dashboard
- 🔍 Transparent voting process

## Technology Stack

- **Backend:** Django 4.2+
- **Frontend:** HTML5, CSS3, JavaScript
- **Database:** MySQL
- **Additional Libraries:** 
  - Pandas (for data handling)
  - Pillow (for image processing)
  - Django Crispy Forms

## Installation Guide

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/st-jude-voting-system.git
   cd st-jude-voting-system
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database**
   - Install and start MySQL
   - Create a database named 'st_jude_voting'
   - Import the initial schema:
     ```bash
     mysql -u root -p st_jude_voting < st_jude_voting.sql
     ```

5. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Update the following variables:
     ```
     SECRET_KEY=your_secret_key
     DEBUG=True
     DB_NAME=st_jude_voting
     DB_USER=your_db_user
     DB_PASSWORD=your_db_password
     EMAIL_HOST_USER=your_email@gmail.com
     EMAIL_HOST_PASSWORD=your_app_specific_password
     ```

6. **Run migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

Visit `http://localhost:8000` to access the application.

## Project Structure

```
st_jude_voting_system/
├── election/                 # Main application directory
│   ├── admin.py             # Admin interface customization
│   ├── models.py            # Database models
│   ├── views.py             # View logic
│   └── urls.py              # URL routing
├── static/                   # Static files (CSS, JS, images)
├── templates/               # HTML templates
├── media/                   # User-uploaded files
└── st_jude_voting_system/   # Project settings
```

## Partnership & Attribution

This project is developed under the collaborative program between:

- **JR Institute of Information Technology**
  - Providing technical expertise and mentorship
  - Supporting youth technology education initiatives

- **The School of St Jude**
  - Project initiation and requirements
  - Testing and implementation environment
  - Student engagement and feedback

## Credits

- **Project Initiator:** Miss Elizabeth (School of St Jude Tech Facilitator)
- **Development:** PearlK Tech
- **Technical Support:** JR Institute of Information Technology(CoderDojo Club)
- **Student Contributors:** School of St Jude Tech Club

## Contact

For inquiries about the partnership program:
- JR Institute of Information Technology - [admin@jriit.ac.tz]
- The School of St Jude - [info@theschoolofstjude.ac.tz]

For technical questions:
- Humphrey  - [humphrey@3ts.co.tz]
- Christopher B - [chriss@3ts.co.tz]
- Miss Elizabeth - [elizabeth.a@theschoolofstjude.ac.tz]
- PearlK Tech - [pearlktech@gmail.com]

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
Made with ❤️ for School of St Jude | A JR Institute - St Jude Partnership Initiative

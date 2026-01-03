# Building an OYO Clone: A Complete Django Hotel Booking System Tutorial

## Table of Contents
1. [Introduction](#introduction)
2. [Project Overview](#project-overview)
3. [Prerequisites](#prerequisites)
4. [Step 1: Environment Setup](#step-1-environment-setup)
5. [Step 2: Creating Django Project](#step-2-creating-django-project)
6. [Step 3: Project Configuration](#step-3-project-configuration)
7. [Step 4: Creating Django Apps](#step-4-creating-django-apps)
8. [Step 5: Database Models Design](#step-5-database-models-design)
9. [Step 6: Migrations and Database Setup](#step-6-migrations-and-database-setup)
10. [Step 7: URL Configuration](#step-7-url-configuration)
11. [Step 8: Views and Business Logic](#step-8-views-and-business-logic)
12. [Step 9: Templates and Frontend](#step-9-templates-and-frontend)
13. [Step 10: Authentication System](#step-10-authentication-system)
14. [Step 11: Key Features Implementation](#step-11-key-features-implementation)
15. [Step 12: Static and Media Files](#step-12-static-and-media-files)
16. [Step 13: Email Configuration](#step-13-email-configuration)
17. [Testing the Application](#testing-the-application)
18. [Conclusion](#conclusion)

---

## Introduction

This tutorial will guide you through building a complete hotel booking system similar to OYO using Django. You'll learn how to create a web application with user authentication, hotel management, booking functionality, and a vendor dashboard.

By the end of this tutorial, you'll have:
- A working hotel booking platform
- User and vendor authentication systems
- Email verification functionality
- Hotel CRUD operations
- Booking management system
- Search and filtering capabilities

---

## Project Overview

Our OYO clone will have two main user types:
1. **Regular Users (HotelUser)**: Can browse hotels, search, filter, and make bookings
2. **Vendors (HotelVendor)**: Can register, manage their hotels, upload images, and view bookings

### Key Features:
- User registration and login (password-based and OTP-based)
- Email verification system
- Hotel listing with search and sort functionality
- Hotel details page with booking form and image gallery
- Vendor dashboard for hotel management
- Image upload and management (during hotel creation and separately)
- Booking system with date calculation and validation
- Customer bookings management (view and cancel bookings)
- Vendor bookings view (view all bookings for vendor's hotels)
- Duplicate booking prevention (same user, same hotel, overlapping dates)
- Admin panel for hotel management (delete, activate/deactivate hotels)

---

## Prerequisites

Before starting, ensure you have:
- Python 3.8+ installed
- Basic knowledge of Python
- Understanding of HTML, CSS, and Bootstrap
- Familiarity with Django basics (models, views, templates, URLs)
- A code editor (VS Code, PyCharm, etc.)
- Git (optional but recommended)

---

## Step 1: Environment Setup

### 1.1 Create a Virtual Environment

First, create a directory for your project and set up a virtual environment:

```bash
mkdir oyo_clone_project
cd oyo_clone_project
python -m venv venv
```

### 1.2 Activate Virtual Environment

**On Windows:**
```bash
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

### 1.3 Install Required Packages

Install Django and other necessary packages:

```bash
pip install django==5.0.7
pip install python-decouple
pip install django-debug-toolbar
```

**Note:** You'll also need to configure email settings. We'll use Gmail SMTP, so ensure you have an app password ready.

---

## Step 2: Creating Django Project

### 2.1 Create Project

Once Django is installed, create a new Django project:

```bash
django-admin startproject oyo_clone
cd oyo_clone
```

This creates a directory structure with:
- `oyo_clone/` - Main project directory
  - `settings.py` - Project settings
  - `urls.py` - Root URL configuration
  - `wsgi.py` - WSGI configuration
  - `asgi.py` - ASGI configuration

### 2.2 Verify Installation

Test if the project was created successfully:

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` - you should see the Django welcome page.

---

## Step 3: Project Configuration

### 3.1 Update Settings

Open `oyo_clone/settings.py` and configure the following:

**INSTALLED_APPS**: Add your apps (we'll create them next) and debug toolbar:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home',
    'accounts',
    'debug_toolbar',
]
```

**MIDDLEWARE**: Add debug toolbar middleware at the top:

```python
MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    # ... other middleware
]
```

**Static and Media Files Configuration**:

```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

**Email Configuration** (for email verification):

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
```

**Note:** Create a `.env` file in the project root with your email credentials:
```
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

---

## Step 4: Creating Django Apps

Our project will have two main apps:

### 4.1 Create Accounts App

This app handles all authentication and user-related functionality:

```bash
python manage.py startapp accounts
```

### 4.2 Create Home App

This app handles the main website functionality (hotel listing, details):

```bash
python manage.py startapp home
```

### 4.3 App Structure

After creating apps, your directory structure should look like:

```
oyo_clone/
├── accounts/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   └── urls.py (create this)
├── home/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   └── urls.py (create this)
└── oyo_clone/
    └── ...
```

---

## Step 5: Database Models Design

### 5.1 Understanding the Data Model

Let's design our database schema. Open `accounts/models.py` and create the following models:

#### User Models

**HotelUser**: Extends Django's User model for regular customers
- Additional fields: profile_picture, phone_number, email_token, otp, is_verified
- Used for customer authentication and bookings

**HotelVendor**: Extends Django's User model for hotel owners
- Additional fields: phone_number, profile_picture, email_token, otp, business_name, is_verified
- Used for vendor authentication and hotel management

#### Core Models

**Ameneties**: Store hotel amenities (WiFi, Pool, Gym, etc.)
- Fields: amenetie_name, icon

**Hotel**: The main hotel model
- Fields: hotel_name, hotel_description, hotel_slug, hotel_owner (FK), ameneties (M2M), hotel_price, hotel_offer_price, hotel_location, is_active
- Relationships: Owner → HotelVendor, Ameneties → ManyToMany

**HotelImages**: Store multiple images for each hotel
- Fields: hotel (FK), image

**HotelManager**: Store manager details for hotels
- Fields: hotel (FK), manager_name, manager_contact

**HotelBooking**: Store booking information
- Fields: hotel (FK), booking_user (FK), booking_start_date, booking_end_date, booking_price

### 5.2 Model Relationships Explained

1. **One-to-Many**: One HotelVendor can own multiple Hotels
2. **Many-to-Many**: Hotels can have multiple Ameneties, and Ameneties can belong to multiple Hotels
3. **One-to-Many**: One Hotel can have multiple HotelImages
4. **One-to-Many**: One Hotel can have multiple HotelBookings

### 5.3 Model Meta Options

Use `db_table` in Meta class to customize table names:
```python
class Meta:
    db_table = "hotel_user"  # Custom table name
```

**Key Points:**
- Use `unique=True` for phone_number to prevent duplicates
- Use `null=True, blank=True` for optional fields like email_token and otp
- Foreign keys use `on_delete=models.CASCADE` for proper data integrity
- Use `related_name` to access reverse relationships easily

---

## Step 6: Migrations and Database Setup

### 6.1 Create Migrations

After defining models, create migration files:

```bash
python manage.py makemigrations
```

This analyzes your models and creates migration files in `accounts/migrations/`.

### 6.2 Apply Migrations

Apply migrations to create database tables:

```bash
python manage.py migrate
```

This creates all tables in your SQLite database (`db.sqlite3`).

### 6.3 Register Models in Admin

Open `accounts/admin.py` and register models to access them via Django admin:

```python
from django.contrib import admin
from .models import *

admin.site.register(HotelUser)
admin.site.register(HotelVendor)
admin.site.register(Ameneties)

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('hotel_name', 'hotel_owner', 'hotel_location', 'hotel_price', 'hotel_offer_price', 'is_active')
    list_filter = ('is_active', 'hotel_owner')
    search_fields = ('hotel_name', 'hotel_location', 'hotel_slug')
    readonly_fields = ('hotel_slug',)
    list_editable = ('is_active',)

@admin.register(HotelImages)
class HotelImagesAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'image')
    list_filter = ('hotel',)
    search_fields = ('hotel__hotel_name',)

@admin.register(HotelBooking)
class HotelBookingAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'booking_user', 'booking_start_date', 'booking_end_date', 'booking_price')
    list_filter = ('booking_start_date', 'booking_end_date')
    search_fields = ('hotel__hotel_name', 'booking_user__email', 'booking_user__first_name', 'booking_user__last_name')
    date_hierarchy = 'booking_start_date'
```

**Admin Features:**
- Hotels can be deleted, activated/deactivated from admin panel
- Search and filter functionality for all models
- Date hierarchy for bookings

### 6.4 Create Superuser

Create an admin user to access Django admin panel:

```bash
python manage.py createsuperuser
```

Follow prompts to set username, email, and password.

---

## Step 7: URL Configuration

### 7.1 Root URL Configuration

In `oyo_clone/urls.py`, include app URLs and configure media/static files:

```python
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

### 7.2 Accounts App URLs

Create `accounts/urls.py` and define authentication and vendor routes:

**Patterns to include:**
- Login/Register routes
- OTP-based login routes
- Email verification route
- Vendor authentication routes
- Vendor dashboard routes
- Hotel management routes (add, edit, upload images)
- Booking view routes

**URL Pattern Examples:**
- `login/` - User login page
- `register/` - User registration
- `login-with-otp/` - OTP login page
- `verify-account/<token>` - Email verification
- `vendor-login/` - Vendor login
- `vendor-register/` - Vendor registration
- `vendor-dashboard/` - Vendor dashboard
- `add-hotel/` - Add new hotel (with image upload)
- `view-bookings/` - View bookings for vendor's hotels
- `<slug>/upload-image` - Upload hotel images separately
- `<slug>/edit-hotel-details/` - Edit hotel details
- `<id>/delete-image/` - Delete hotel image

### 7.3 Home App URLs

Create `home/urls.py` for main website routes:

- `''` - Home page (hotel listing)
- `my-bookings/` - Customer bookings page (view and manage bookings)
- `cancel-booking/<booking_id>/` - Cancel a booking
- `<slug>/hotel-details` - Hotel details page with image gallery

**Key Concept**: Use slug-based URLs for SEO-friendly hotel detail pages instead of IDs.

---

## Step 8: Views and Business Logic

### 8.1 View Structure

Views handle HTTP requests and return responses. We'll use function-based views for this project.

### 8.2 Authentication Views (Accounts App)

#### Login View
- Handle GET request: Display login form
- Handle POST request: 
  - Validate email exists
  - Check if user is verified
  - Authenticate user with username and password
  - Login and redirect to home

#### Register View
- Handle GET request: Display registration form
- Handle POST request:
  - Check if email/phone already exists
  - Create HotelUser instance
  - Generate email token using UUID
  - Set password securely
  - Send verification email
  - Show success message

#### OTP Login Flow
1. **login_with_otp_view**: Display email input form
2. **login_otp_enter_view**: 
   - Generate random 4-digit OTP
   - Save OTP to user model
   - Send OTP via email
   - Display OTP input form
3. **verify_otp_view**: 
   - Compare entered OTP with saved OTP
   - If match, login user
   - If mismatch, show error and return to OTP form

#### Email Verification View
- Extract token from URL
- Find user (HotelUser or HotelVendor) by email_token
- Set is_verified = True
- Redirect to appropriate login page

### 8.3 Vendor Views

#### Vendor Dashboard
- Filter hotels by logged-in vendor
- Attach images to hotels (helper function)
- Display hotels with pagination

#### Add Hotel View
- GET: Display form with amenities list
- POST:
  - Extract form data
  - Validate required fields
  - Generate unique slug from hotel name
  - Create Hotel instance
  - Add amenities (ManyToMany relationship)
  - Handle multiple image uploads (optional)
  - Create HotelImages instances for uploaded images
  - Show success message with image count
  - Redirect to vendor dashboard

#### Edit Hotel View
- GET: Display form pre-filled with hotel data
- POST:
  - Update hotel fields
  - Handle amenities update
  - Save changes

#### Upload Images View
- Display existing images
- Handle file upload
- Create HotelImages instance
- Redirect to same page (refresh)

#### View Bookings View (Vendor)
- Filter bookings for hotels owned by the vendor
- Calculate booking duration for each booking
- Display customer name, hotel, dates, price, and location
- Order bookings by date (newest first)

### 8.4 Home Views

#### Index View (Hotel Listing)
- Query all active hotels
- Apply search filter if provided
- Apply sorting (low to high / high to low)
- Use select_related and prefetch_related for optimization
- Attach images using helper function
- Render template with hotel list

**Query Optimization Tip**: Use `select_related()` for ForeignKey and `prefetch_related()` for ManyToMany to reduce database queries.

#### Hotel Details View
- Get hotel by slug with prefetch_related for images and amenities
- Display hotel images in gallery format
- Handle booking POST request:
  - Validate dates are provided
  - Validate date format
  - Validate end date is after start date
  - Check if user is a HotelUser (not vendor)
  - Check for overlapping bookings (prevent duplicates)
  - Calculate number of days
  - Calculate total price (offer_price × days, rounded to 2 decimals)
  - Create HotelBooking instance
  - Show success message
  - Redirect to my-bookings page
- Pass today's date for date picker min value

#### My Bookings View (Customer)
- Filter bookings for logged-in customer
- Calculate booking duration for each booking
- Display hotel name, location, dates, price
- Order bookings by date (newest first)
- Include cancel booking functionality

#### Cancel Booking View
- Verify booking belongs to logged-in user
- Delete booking from database
- Show success/error message
- Redirect to my-bookings page

### 8.5 Helper Functions

#### setImages Function
- Purpose: Attach image URLs to hotel objects
- Logic: Get the first image from each hotel's own hotel_images relationship
- Used in: Index view, vendor dashboard
- Improvement: Now uses hotel's own images instead of shared/random images

#### generate_slug Function
- Purpose: Create unique URL-friendly slugs
- Logic: Combine slugified hotel name with UUID segment
- Handles: Duplicate slug checking with recursion

---

## Step 9: Templates and Frontend

### 9.1 Template Structure

Create template directories:
```
accounts/templates/
├── login.html
├── register.html
├── login_otp.html
└── vendor/
    ├── vendor_login.html
    ├── vendor_register.html
    ├── vendor_dashboard.html
    ├── add_hotel.html
    ├── edit_hotel_details.html
    ├── upload_image.html
    └── view_bookings.html

home/templates/
├── index.html
├── hotel_details.html
├── my_bookings.html
└── utils/
    ├── base.html
    ├── navbar.html
    └── alerts.html
```

### 9.2 Base Template

Create `home/templates/utils/base.html`:
- Include Bootstrap CSS/JS
- Include navbar
- Include alert messages
- Define `{% block start %}` for page content

### 9.3 Key Template Concepts

**Template Inheritance**: Use `{% extends %}` to inherit from base template

**Context Variables**: Access data passed from views using `{{ variable }}`

**Template Tags**: Use `{% for %}`, `{% if %}`, `{% url %}` for logic

**CSRF Protection**: Always include `{% csrf_token %}` in forms

**Static Files**: Use `{% load static %}` and `{% static 'path' %}` for CSS/JS/images

### 9.4 Form Handling in Templates

**Login Form Example Structure:**
- Method: POST
- Action: Same URL or use `{% url 'login' %}`
- Include CSRF token
- Input fields with name attributes
- Submit button

**Search Form (GET method):**
- Use GET for search (bookmarkable URLs)
- Access via `request.GET.get('search')`

### 9.5 Displaying Data

**Hotel Listing:**
- Loop through hotels using `{% for hotel in hotels %}`
- Display hotel information
- Use conditional rendering for images
- Display amenities using nested loop
- Create links to hotel details using slug

**Image Display:**
- Use `{{ hotel.image_url }}` for dynamic images
- Provide fallback image if no image exists
- Use Bootstrap classes for styling

---

## Step 10: Authentication System

### 10.1 Custom User Models

**Why extend User model?**
- Django's default User model may not have all fields we need
- We need separate models for customers and vendors
- Additional fields: phone_number, email_token, otp, etc.

**Implementation Approach:**
- Inherit from `django.contrib.auth.models.User`
- Add custom fields
- Use custom table names via Meta class

### 10.2 Authentication Flow

#### Registration Flow:
1. User fills registration form
2. Check if email/phone already exists
3. Create user instance with email_token
4. Set password (use `set_password()` for hashing)
5. Send verification email with token link
6. User clicks link → Email verified
7. User can now login

#### Login Flow (Password-based):
1. User enters email and password
2. Find user by email
3. Check if verified
4. Authenticate using `authenticate()` function
5. Login using `login()` function
6. Redirect to home page

#### Login Flow (OTP-based):
1. User enters email
2. Generate random OTP (4 digits)
3. Save OTP to user model
4. Send OTP via email
5. User enters OTP
6. Verify OTP matches
7. Login user

### 10.3 Security Best Practices

- **Password Hashing**: Always use `set_password()` - never store plain passwords
- **CSRF Protection**: Always include CSRF token in forms
- **Email Verification**: Require email verification before allowing login
- **Session Management**: Use Django's built-in session framework
- **Login Required**: Use `@login_required` decorator for protected views

### 10.4 Decorators Usage

```python
@login_required(login_url="vendor-login")
def vendor_dashboard_view(request):
    # Only logged-in vendors can access
    pass
```

---

## Step 11: Key Features Implementation

### 11.1 Email Verification System

**Components:**
1. **Token Generation**: Use UUID4 to generate unique tokens
2. **Email Sending**: Use Django's `send_mail()` function
3. **Verification URL**: Include token in URL parameters
4. **Token Validation**: Lookup user by token and verify

**Email Template Structure:**
- Subject line
- Verification link with token
- User-friendly message

### 11.2 Slug Generation

**Why use slugs?**
- SEO-friendly URLs
- Human-readable
- Better than numeric IDs

**Implementation:**
- Use Django's `slugify()` to convert hotel name
- Append UUID segment for uniqueness
- Check for duplicates recursively

### 11.3 Hotel Search and Filtering

**Search Implementation:**
- Use `icontains` for case-insensitive search
- Filter on hotel_name field
- Preserve search term in URL (GET method)

**Sorting Implementation:**
- Sort by `hotel_offer_price`
- Ascending: `order_by('hotel_offer_price')`
- Descending: `order_by('-hotel_offer_price')`

### 11.4 Booking System

**Booking Logic:**
1. User selects check-in and check-out dates
2. Validate dates are provided and in correct format
3. Validate end date is after start date
4. Check if user is a HotelUser (vendors cannot book)
5. Check for overlapping bookings (prevent duplicate bookings for same hotel/dates)
6. Calculate number of days: `(end_date - start_date).days`
7. Calculate total price: `hotel_offer_price × days` (rounded to 2 decimals)
8. Create HotelBooking instance
9. Store booking with user and hotel relationship
10. Redirect to my-bookings page

**Date Handling:**
- Use `datetime.strptime()` to parse date strings
- Format: `'%Y-%m-%d'` (YYYY-MM-DD)
- Set minimum date in date picker to today
- Validate dates before processing

**Booking Validation:**
- Prevent vendors from booking (only customers can book)
- Prevent duplicate/overlapping bookings for same user and hotel
- Validate date formats and logic

### 11.5 Image Management

**Upload Process:**
1. Handle `request.FILES.getlist('images')` for multiple images
2. Create HotelImages instance for each image
3. Associate with hotel via ForeignKey
4. Django handles file storage automatically
5. Images can be uploaded during hotel creation OR separately later

**Display Process:**
1. Access images via reverse relationship: `hotel.hotel_images.all()`
2. Use `image.url` to get file URL
3. Display in template using `<img>` tag
4. Hotel details page shows all images in a gallery format
5. Vendor dashboard shows first image for each hotel

**File Storage:**
- Files stored in `MEDIA_ROOT/hotels/` directory
- Access via `MEDIA_URL` in templates
- Ensure MEDIA_URL is configured in URLs

### 11.6 Many-to-Many Relationships

**Adding Amenities to Hotel:**
- Get amenity objects by ID
- Use `.add()` method: `hotel.ameneties.add(amenity)`
- Save hotel instance

**Displaying Amenities:**
- Access via reverse relationship: `hotel.ameneties.all()`
- Loop in template to display all amenities

---

## Step 12: Static and Media Files

### 12.1 Static Files Configuration

**Development:**
- Create `static/` directory in project root
- Add to `STATICFILES_DIRS` in settings
- Serve automatically in DEBUG mode

**Usage in Templates:**
```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
```

### 12.2 Media Files Configuration

**Settings:**
- `MEDIA_URL = '/media/'`
- `MEDIA_ROOT = os.path.join(BASE_DIR, 'media')`

**URL Configuration:**
- Add media URL patterns in `urls.py` (only in DEBUG mode)

**File Upload Fields:**
- Use `ImageField` or `FileField` in models
- Specify `upload_to` parameter for directory structure

### 12.3 File Handling Best Practices

- Always validate file types and sizes
- Use appropriate `upload_to` paths
- Handle file deletion when objects are deleted
- Use `MEDIA_URL` in templates, not hardcoded paths

---

## Step 13: Email Configuration

### 13.1 Gmail SMTP Setup

1. Enable 2-Factor Authentication on your Gmail account
2. Generate App Password:
   - Google Account → Security → 2-Step Verification → App Passwords
   - Generate password for "Mail"
3. Store credentials in `.env` file

### 13.2 Environment Variables

Use `python-decouple` to manage sensitive data:

**Install:**
```bash
pip install python-decouple
```

**Create `.env` file:**
```
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
SECRET_KEY=your_secret_key
```

**In settings.py:**
```python
from decouple import config

EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
```

### 13.3 Email Functions

**send_test_email():**
- Purpose: Send verification email
- Parameters: email, token
- Include verification link in message

**send_email_with_otp():**
- Purpose: Send OTP for login
- Parameters: email, otp
- Include OTP in message body

---

## Testing the Application

### Testing Checklist

1. **User Registration:**
   - Register new user
   - Check email for verification link
   - Verify email
   - Try login before verification (should fail)
   - Login after verification (should succeed)

2. **User Login:**
   - Test password-based login
   - Test OTP-based login
   - Test incorrect credentials
   - Test unverified account login

3. **Vendor Functions:**
   - Vendor registration and login
   - Add new hotel
   - Upload hotel images
   - Edit hotel details
   - View bookings

4. **Hotel Listing:**
   - View all hotels
   - Test search functionality
   - Test sorting (low to high, high to low)
   - Click on hotel to view details

5. **Booking System:**
   - Select dates on hotel details page
   - Submit booking
   - Verify booking creation
   - Check booking in my-bookings page (customer)
   - Check booking in vendor view-bookings page
   - Cancel a booking
   - Try to book overlapping dates (should be blocked)
   - Try to book as vendor (should be blocked)

6. **Image Management:**
   - Upload images during hotel creation
   - Upload images separately after creation
   - View images on hotel details page
   - Delete images from vendor dashboard

7. **Edge Cases:**
   - Duplicate email registration
   - Invalid OTP
   - Booking with invalid dates
   - Booking with overlapping dates (should be prevented)
   - Vendor trying to book (should be blocked)
   - Accessing protected views without login
   - Unverified users trying to login (should be blocked)
   - Viewing inactive hotels (should redirect)

### Common Issues and Solutions

**Issue: Static files not loading**
- Solution: Ensure `STATIC_URL` and `STATICFILES_DIRS` are configured correctly
- Run `python manage.py collectstatic` if needed

**Issue: Media files not displaying**
- Solution: Check `MEDIA_URL` and `MEDIA_ROOT` settings
- Ensure media URL patterns are added in `urls.py`

**Issue: Email not sending**
- Solution: Verify email credentials in `.env` file
- Check app password is correct
- Ensure EMAIL settings are properly configured

**Issue: Migration errors**
- Solution: Delete migration files (except `__init__.py`) and `db.sqlite3`
- Run `makemigrations` and `migrate` again

---

## Conclusion

Congratulations! You've built a complete hotel booking system with:

✅ User and vendor authentication  
✅ Email verification system  
✅ Hotel CRUD operations  
✅ Image management (upload during creation and separately)  
✅ Search and filtering  
✅ Booking system with validation  
✅ Customer bookings management (view and cancel)  
✅ Vendor bookings view  
✅ Duplicate booking prevention  
✅ Vendor dashboard  
✅ Admin panel for hotel management  

### Key Learnings

1. **Django Project Structure**: Understanding apps, models, views, templates, URLs
2. **Database Design**: Relationships (One-to-Many, Many-to-Many), Foreign Keys
3. **Authentication**: Custom user models, login, registration, email verification
4. **File Handling**: Image uploads, static and media files
5. **Forms**: GET/POST handling, CSRF protection, form validation
6. **Query Optimization**: select_related, prefetch_related
7. **URL Routing**: Slug-based URLs, URL parameters
8. **Template System**: Inheritance, context variables, template tags

### Next Steps

Consider adding these features to enhance the project:
- Payment gateway integration
- Reviews and ratings system
- Advanced filtering (by location, price range, amenities)
- Email notifications for bookings
- Admin dashboard with analytics
- Booking status management (pending, confirmed, cancelled)
- Refund system for cancellations
- Booking history and analytics
- REST API using Django REST Framework
- Frontend framework integration (React, Vue.js)
- Real-time notifications
- Hotel availability calendar

### Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Tutorial](https://docs.djangoproject.com/en/stable/intro/tutorial01/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)

---

**Happy Coding! 🚀**

---

*Note: This tutorial provides a comprehensive overview of building the OYO clone. For complete source code implementation, refer to the provided codebase. Focus on understanding the concepts and architecture rather than memorizing code snippets.*


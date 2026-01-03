from accounts.models import Hotel, HotelVendor, Ameneties, HotelImages
from accounts.templates.utils.sendEmail import generate_slug
from faker import Faker
from django.conf import settings
from django.core.files import File
import random
import os

fake = Faker()


def generate_fake_hotel(total_hotels=100, reset=True):

    # 🔴 STEP 0: DELETE EXISTING HOTELS (ONLY ONCE)
    if reset:
        HotelImages.objects.all().delete()
        Hotel.objects.all().delete()
        print("🗑️ Existing hotels & images deleted")

    # 1️⃣ Get any existing vendor
    hotel_vendor = HotelVendor.objects.first()
    if not hotel_vendor:
        print("❌ No HotelVendor found. Create one from admin first.")
        return

    # 2️⃣ Get all amenities
    amenities = list(Ameneties.objects.all())
    if not amenities:
        print("❌ No amenities found. Create amenities first.")
        return

    # 3️⃣ Image seed folder
    seed_image_dir = os.path.join(settings.MEDIA_ROOT, "hotels_seed")
    if not os.path.exists(seed_image_dir):
        print("❌ media/hotels_seed folder not found")
        return

    image_files = [
        f for f in os.listdir(seed_image_dir)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    if not image_files:
        print("❌ No images found in media/hotels_seed")
        return

    # 4️⃣ Create hotels with images
    for _ in range(total_hotels):
        hotel_name = fake.company() + " Hotel"
        hotel_description = fake.text(max_nb_chars=200)
        hotel_price = round(random.uniform(1000, 5000), 2)
        hotel_offer_price = round(hotel_price * random.uniform(0.6, 0.9), 2)
        hotel_location = fake.address().replace("\n", ", ")

        hotel = Hotel.objects.create(
            hotel_name=hotel_name,
            hotel_description=hotel_description,
            hotel_slug=generate_slug(hotel_name),
            hotel_owner=hotel_vendor,
            hotel_price=hotel_price,
            hotel_offer_price=hotel_offer_price,
            hotel_location=hotel_location,
        )

        # Amenities
        hotel.ameneties.add(
            *random.sample(amenities, min(len(amenities), random.randint(3, 6)))
        )

        # Images
        for img_name in random.sample(
            image_files,
            min(len(image_files), random.randint(3, 6))
        ):
            img_path = os.path.join(seed_image_dir, img_name)
            with open(img_path, "rb") as img:
                HotelImages.objects.create(
                    hotel=hotel,
                    image=File(img, name=img_name)
                )

    print(f"✅ {total_hotels} hotels re-seeded with images successfully")

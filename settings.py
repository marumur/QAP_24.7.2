import os

from dotenv import load_dotenv

load_dotenv()



valid_email = os.getenv('valid_email')
valid_password = os.getenv('valid_password')

invalid_email = os.getenv('invalid_email')
invalid_password = os.getenv('invalid_password')

name1 = 'Масюк'
animal_type1 = 'кот'
age1 = 6
pet_photo1 = 'images/masyuk.jpg'

name2 = 'Сына'
animal_type2 = 'кот'
age2 = 13
pet_photo2 = 'images/syna.jpg'

pet_photo3 = 'images/The_Office.torrent' #incorrect type of photo

name49 = 'cTxBDH0IbZqKicPFhL8y23UJLIyB59S3p1hqVIa3nYjSZKdr8'
name50 = 'Haxqfifg6HGZJB0jUuEEF13yFlPOIDKvM5vrEUvh24PS0AJLwH' #name consists of 50 characters
name51 = 'o1PsDwg5uo7BHXswSBTuVSxRHUxiVc0LDqlcSFLlP77Z56vv6dE'
name99 = 'CSZtF6PimnEhEYp73kMMZklJvN9JJfUFLeSTzGpghwHSPP3trCKsGzuzr8ilfmoX1Za09SyocelrwCuVxMnW6ThQZbjkpwTKXpA'
name100 = 'EJGwJmLE0y0DhX5soerQOUgx6ixV8aaoRDnkLvmrzI5do8TRNT97QwtxqcQPeLf3JP133tNglPgKodiYbvimt0WPJ9HFkX14wxMO'
name101 = '2khkqZoqSqX3OY96FnBbqi5MvN1EnPkiDckXnjiBbyqB9SeRnjKnH3f0naLghCpoNBeQe9I6K7GuP0ZLR6ibcDvudZDAowdTvvDCG'
name_empty = ''

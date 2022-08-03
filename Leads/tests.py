from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth import get_user_model


from Leads.models import Lead

User = get_user_model()


class LandingPageTest(TestCase):
    def setUp(self):
        # creating a user
        self.user = User.objects.create_user(username='Michael', password='yourchoice')
        
         # agent user
        self.user2 = User.objects.create_user(username="James", password='goodboy')
        self.user2.is_organizer = False
        self.user2.is_agent = True


        #creating a lead and assigning the organizer to the created organizer user
        self.created_lead_user = Lead.objects.create(first_name='Jude',
                                                     last_name='Asamoah', age='10',
                                                     description='This is a test lead',
                                                     phone_number='0559393030',
                                                     email='testemail@gmail.com',
                                                     profile_pictures="null",
                                                     organization = self.user.userprofile
                                                     )


    # testing the organizer user and agent user
    def test_user_created(self):
        self.assertEqual(self.user.username, "Michael")
        self.assertEqual(self.user.is_organizer, True)
        
        self.assertEqual(self.user2.username, "James")
        self.assertEqual(self.user2.is_agent, True)


    #testing the created lead
    def test_lead_created(self):
        self.assertEqual(self.created_lead_user.age, '10')
        self.assertEqual(self.created_lead_user.organization, self.user.userprofile)



    def test_get(self):
       response = self.client.get(reverse("Leads:Landing_page"))
       self.assertEqual(response.status_code, 200)
       self.assertTemplateUsed(response, "landing.html")


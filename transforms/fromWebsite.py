from maltego_trx.transform import DiscoverableTransform
from maltego_trx.entities import Person, Email, Location, PhoneNumber,  Alias, URL
from extensions import registry, URLscraper_set
from URLscrapper import get_data


@registry.register_transform(display_name="From Website [URLscrapter]", 
                             input_entity="maltego.Website", 
                             description="Finds names, emails, phones, geolocations, usernames, social link from website", 
                             output_entities=["maltego.Person", "maltego.Email", "maltego.PhoneNumber", "maltego.Location", "maltego.URL"],
                             transform_set=URLscraper_set)
class fromWebsite(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request, response):
        from_website = request.Value

        data = []
        # get output data
        try:
            data = get_data(from_website)
        except:
            return
        
        for d in data:
            source = d['source']
            details = d['data']
        
            # create entities
            # emails
            for email in details['email_addresses']:
                ent = response.addEntity(Email, email)
                ent.setLinkThickness(1)
                ent.setLinkLabel("urlstrapper")
                ent.addCustomLinkProperty('page', 'Page URL', source)
            
            # author_names
            for name in details['author_names']:
                ent = response.addEntity(Person, name)
                ent.setLinkThickness(1)
                ent.setLinkLabel("urlstrapper")
                ent.addCustomLinkProperty('page', 'Page URL', source)

            # geolocation
            for location in details['geolocations']:
                ent = response.addEntity(Location, location)
                ent.setLinkThickness(1)
                ent.setLinkLabel("urlstrapper")
                ent.addCustomLinkProperty('page', 'Page URL', source)

            # phone numbers
            for phone in details['phone_numbers']:
                ent = response.addEntity(PhoneNumber, phone)
                ent.setLinkThickness(1)
                ent.setLinkLabel("urlstrapper")
                ent.addCustomLinkProperty('page', 'Page URL', source)

            # usernames
            for username in details['usernames']:
                ent = response.addEntity(Alias, username)
                ent.setLinkThickness(1)
                ent.setLinkLabel("urlstrapper")
                ent.addCustomLinkProperty('page', 'Page URL', source)

            # social links
            for platform, link in details['social_links'].items():
                ent = response.addEntity(URL, platform)
                ent.addProperty('url', 'URL', 'loose', link)
                ent.setLinkThickness(1)
                ent.setLinkLabel("urlstrapper")
                ent.addCustomLinkProperty('page', 'Page URL', source) 

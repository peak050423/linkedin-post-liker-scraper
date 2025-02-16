from apify import Actor
from datetime import datetime
import platform
from .post_likers import getLikersList

def get_current_timestamp():
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime('%#m-%d-%Y_%#I-%M-%p')

    return formatted_datetime

async def main():
    async with Actor:
        # Get the value of the actor input
        actor_input = await Actor.get_input() or {}

        # Structure of input is defined in .actor/input_schema.json
        post_url = actor_input.get('post_url')
        linkedin_cookies = actor_input.get('cookies')

        if post_url is None:
            raise ValueError('Post Url parameter is required')
        if linkedin_cookies is None:
            raise ValueError("Cookies parameter is required")


        current_timestamp = get_current_timestamp()
        cookies = {cookie['name']: cookie['value'] for cookie in linkedin_cookies}
        result = []

        likers_info = getLikersList(post_url, current_timestamp, cookies)

        if not likers_info:
            raise ValueError('No data found')

        result = likers_info

        # Structure of output is defined in .actor/actor.json
        print(f'post_url: {post_url}')

        for row in result:
            await Actor.push_data(
            {
                "fullName": row.get('fullName'),
                "jobTitle": row.get('jobTitle'),
                "profileUrl": row.get('profileUrl'),
                "imageUrl": row.get('imageUrl'),
                "connectionDegree": row.get('connectionDegree'),
                "timestamp": current_timestamp,
                "positionTitle": row.get('positionTitle'),
                "companyLogo": row.get('companyLogo'),
                "companyName": row.get('companyName'),
                "locationName": row.get('locationName')
            }
        )

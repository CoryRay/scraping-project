import json
import typer
from rich import print
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from TideScraper import TideScraper

console = Console()


def main():
    print(get_content('welcome'))

    # show available options
    table = Table("Number", "Location")
    for index, loc in enumerate(locations):
        table.add_row(str(index), loc[0])
    console.print(table)

    location_index = Prompt.ask(get_content('choice'))

    # make sure input is valid
    try:
        # Ensure it's an int
        location_index = int(location_index)
    except:
        print(get_content('invalid_index'))
        raise typer.Exit()

    # Ensure it's a valid index
    if not 0 <= location_index < len(locations):
        print(get_content('invalid_location'))
        raise typer.Exit()

    selected_location_name = locations[location_index][0]

    # is this what user wanted?
    confirm = Confirm.ask(get_content('confirm', selected_location_name))
    if not confirm:
        raise typer.Exit()

    tide_days = get_scraped_data(locations[location_index][1])

    # build table to show
    table = Table("Date", "Low Tide Time", "Height")
    for day in tide_days:
        sunrise = day['sunrise']
        sunset  = day['sunset']

        for tide in day['tides']:
            if tide['type'] == 'low':
                if tide['timestamp'] > sunrise and tide['timestamp'] < sunset:
                    table.add_row(day['date'], tide['time'], "{:.2f}ft".format(tide['height']))

    print(get_content('present', selected_location_name))
    console.print(table)
    print(get_content('bye'))
    # program done

def get_scraped_data(city_url: str):
    url_data = TideScraper.get_url_data(city_url)
    data = json.loads(url_data[0])

    # return JSON to build a table to display
    return data['tideDays'] # we only need data in tideDays

# There's probably a better way to store these
# Brittle if URL structure changes
locations = [
    ["Half Moon Bay, California", "https://www.tide-forecast.com/locations/Half-Moon-Bay-California/tides/latest"],
    ["Huntington Beach, California", "https://www.tide-forecast.com/locations/Huntington-Beach/tides/latest"],
    ["Providence, Rhode Island", "https://www.tide-forecast.com/locations/Providence-Rhode-Island/tides/latest"],
    ["Wrightsville Beach, North Carolina", "https://www.tide-forecast.com/locations/Wrightsville-Beach-North-Carolina/tides/latest"],
]
def get_content(index: str, input: str = None) -> str:
    content = {
        'welcome': 'Welcome! Please choose a location to see [bold green]low tides[/bold green] during [bold green]daylight hours[/bold green] from the selection below.',
        'choice': 'Which location would you like to see times for?',
        'confirm': f'You selected [bold green]{input}[/bold green], is this correct?',
        'invalid_index': 'You didn\'t even pick a number...',
        'invalid_location': 'This location does not exist.',
        'present': f'Here are the daytime low tide times for [bold green]{input}[/bold green]:',
        'bye': 'Now go explore the tide pools!'
    }
    return content[index]

if __name__ == "__main__":
    typer.run(main)

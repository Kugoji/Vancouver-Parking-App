# Vancouver Parking App
A fun project of mine where I made an app that shows the nearest parking meters in **Vancouver, BC** relative to the user's location while also displaying important info about the meter.  
Here's the link to interact with the app directly: https://van-parking-meters.streamlit.app 

## How It's Made
**Tech & Libraries used:** `Python`, `Streamlit`, `Pandas`, `Numpy`, `Folium`  

To make this app, I did the coding within `Python`, utilizing the `streamlit` library in order to design the front-end. The app is based on parking meter data sourced directly from `The City of Vancouver Open Data Portal` and as such, has a very comprehensive selection of all the parking meters within the city. 

To use this app, the user must first select the `day` and `time` they would like to park. The user can also decide to show only parking meters that have `credit cards` as a form of payment. If left empty, the app will show **all meters** that match the other selected criteria, **regardless of the forms of payment they offer**. From there, the user must then allow their location to be shared as the app will use the user's location to display all the parking meters based on **proximity**. 

The user can then select one of the displayed `parking meter ID's` and view information specific to that meter such as the: 
- rate of the meter (CAD/Hour)
- time limit of the meter (Hours)
- distance (km)
- estimated walking time (min)
- name of the neighbourhood where the meter is located
- type of meter
- types of payment the meter allows  

Once a `meter ID` is selected, an interactive map made via `folium` will also be displayed. An `indicator icon` will show the location of the **parking meter** and the **user**, with a `path` being displayed on how to reach the meter. By clicking the `path`, the `distance` and `estimated walking time` will be displayed.

The app does not automatically register the user's current location so in order to display the user's updated position and other details that come with that, a quick refresh of the page is necessary.  

## Lessons Learned 
As someone who had a basic level of proficiency with `Python` and `streamlit` prior to this project, I learned a lot during the entire process! I had made a web-app using `Python` and `streamlit` before, but it was primarily used as a display of statistical modelling. The process of creating an app where people would potentially be using it in a casual setting was new to me and required a different approach of thinking. I had to focus on not only the rigor/accuracy of my results, but how feasible it would be for someone to utilize. Due to these challenges, throughout the making of the app, I greatly improved my product strategy skills. From a technical perspective, I utilized many libraries I wasn't familliar with such as `streamlit_geolocation` for caching the user's location and `folium` for building the maps. There was definitley a lot of trial-and-error when it came to making sure the app functioned in a way that I wanted, and due to my coding skills being limited to just `Python` and `streamlit`, there were certain limitations I had to find work-arounds for, but ultimately, those were some of the things that made this project engaging and fun!


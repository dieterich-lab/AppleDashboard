# Create/ Remove a new tab/app

Apple Dashboard app uses plotly Dash to create a Dashboard. 
The instructions on how to create a Dashboard using plotly can be found at this [link](https://dash.plotly.com/)

To create/ remove a tab, follow these steps:

1. Create/ delete a file in the [apps directory](https://github.com/dieterich-lab/AppleDashboard/tree/master/apps) 

    1.1 Create layout and callbacks for new tab in the created file.
    
    1.2 If the file grow to large, it is recommended to create additional files for the functions.

2. Add/ Remove a link in the `index.py` file

    1.1 Import the file/app that was created in the apps folder
    
    1.2 Find the Card with all the links in the layout and add the dcc.Link component
    
    1.3 Update the callback by adding dcc.Link component to the tab
    
    1.4 Return layout and tab if path is selected

3. Customize the appearance of tabs in assets/s1.css file find `.tabs > a { width: 24%;}`
    
### Create new chart new table inside of app ###

1. Add a new dcc component to the layout in one of the apps eg.`AppleWatch.py`
2. Add a callback for the created dcc component if necessary
3. If additional calculations are needed it is recommended to create an additional function file to make the code easier to read.
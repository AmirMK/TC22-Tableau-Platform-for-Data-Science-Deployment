# TC22-Tableau-Platform-for-Data-Science-Deployment
## Heading 2
* Tableau Desktop 22.1
* Python with the following packages: TabPy (http://pip install tabpy)and ortools (https://pypi.org/project/ortools/)
    * Having TabPy up and run on your machine
    * Connect Tableau to the TabPy


* Python IDE
* Step 0 - 

* Run TabPy on your VM/machine and make sure Tableau Desktop is connected to the TabPy Server:
Have the starter workbook open:

## Business Problem:
A telecommunication company has planned to expand its coverage in some California counties by installing cellular towers.  There are multiple potential locations to install the new towers, each of which has its own installation cost as well as population coverage. Given the limited budget, the business wants to find the best locations to install the new towers maximizing the total covered population while keeping installation cost under budget.
### Explore the Solution:
The “*Exploring the solutions*“ dashboard is built by native Tableau’s functionalities such as LOD, dynamic parameters, sets, actions, etc. and there is no external service integration.  This dashboard enables business users to examine different scenarios and understand the impact of each scenario/selection on the two KPIs : cost and covered population. 
This is definitely a great exploration tool; however, as you can imagine, there are countless scenarios possible, which makes it nearly impossible to find the absolute optimal one. To do so, we need to have a mathematical model running in the back-end to intelligently search among all possible scenarios and reports the best one. To achieve that, we are going to build such a model with Python and bring it into Tableau to visualize the solution.
### Optimization Solution:
In this part, we are going to use ortools (https://developers.google.com/optimization/introduction/python), a python open source package developed by Google to solve the optimization problem:
This function gets three arguments: population, cost, and budget, then runs the optimization and returns the optimal solution:
From the data structure perspective, Tableau sends data in the form of “list” to any Python model. So, the Python code/model needs to be written in away that consumes lists as input. In this example, we have three inputs for our model. Two of them naturally are lists, population and cost specified for each region, but budget is a single number, which is global. We are going to use a Tableau parameter to specify the budget. In this situation, Tableau automatically converts the parameter into a list with the same length as population and cost by repeating the same value. In the code, we used Budget[0] to get the first element of the list as a single number. 

In terms of output data, Tableau expects either a list with the same length as the input data or one single number as the output. In this example, the Python model returns a list of True/False values indicating whether a region is selected or not. The output structure is therefore aligned with Tableau and we do not need to make any changes on that end.
### Model Deployment
Now we are going to deploy this function on TabPy to enable business users to call it directly from Tableau. 
Step 1- 

* While TabPy is running, run the python code to build and deploy the model with one of these options:
    * Option 1: Run the code in your Jupyter Notebook:Optimization.ipynb 
    * Option 2: Run the following command from your terminal: Optimization.py 
    * Option 3: Run the following Python code from your IDE:

We used TabPy as deployment platform to operationalize our optimization models and enable business users to call through Tableau. Next step is to bring our models into Tableau.

Step 2-

* From the “*Optimized Solution*” dashboard go to the “*Optimization*” worksheet
* Edit the “*Optimum Assignment*” field
* Copy and paste formula below in the field

MODEL_EXTENSION enables Tableau users to call any deployed model with the analytics extensions API (in this case TabPy) to pass the data and return back the result to build the viz. Tableau sends all the data from the viz as aggregated, and the level of aggregation is the same as the marks on the viz. For example, In Santa Clara Area there are 22 marks on the viz, each mark showing the potential locations to install the towers. So, the population and cost are all aggregated at this level, which makes sense. Although all dimensions and measures are aggregated parameters do not need to be. The only consideration is the form of data. As mentioned earlier, Tableau sends all data in the form of lists to the external models, and the length of each list is the same as the number of mark in the viz. 

For two measures cost and population this format makes sense, since each mark (location) has its own cost and population. However, the parameter representing the budget is one single number. In this case, Tableau automatically generates a list of “n” identical values (n= number of marks on the viz, and the all values are the same as the parameter). Therefore, your code needs to be written in a way that converts the list of identical numbers into one single value (this can be done easily by getting the first element of that list, please note how Budget is used in the python code).
The output of the Python model is a calculation field, so it can be used to build any sort of visualization. For example, in the first layer of the map, it is used as the shape to indicate whether a tower is on/off. In the second layer, we use it as the color to indicate which ares would be covered by the installation strategy. 

After running the model, some of the areas turn green. These are the optimal locations to install your towers, maximizing the covered population while making sure the installation cost is below the total budget. 

Since the result of the model is a calculation field, users can build other calculations based on it. For example, we built ‘Optimum Coverage’ to compute the total covered population based on the result of the model, aka ‘Optimum Assignment’.

* *IMPORTANT NOTE:* Calculation fields with MODEL_EXTENSION functions are considered as “Table Calculations” so defining the correct dimension plays a critical role in performance as well as concreteness of result.
    * In the viz, “Coverage Zone” and “State” are specified as dimensions for “Optimum Assignment”, which means Tableau will NOT partition the data by any of these dimensions and send all data at once to the model. Otherwise, Tableau runs the optimization model for each coverage region individually, which does not make sense.

    * On the other hand, “Region” was not specified as a dimension, because in the case of having multiple regions in the viz, we want to optimize the installation in each region independently and not all at once. 
            * (Optional) You may change the filter to multiple selection and select multiple region (like Santa Clara Area and South Superior California). Tableau runs the optimization model for each region separately.  
            * (Optional) You may try to add “Region” to dimension. How does it impact the solution?  
            * Here (https://www.tableau.com/about/blog/2018/8/working-external-services-tableau-tabpy-r-matlab-93351?_ga=2.59834414.2043646915.1648567682-998224787.1648567682)is a good reference to learn more about “Table Calculation.”

Step 3- Let’s use the tool to answer the following business questions:

    * How much coverage will you  gain/lose by increasing/decreasing your total budget by +/-$10M?
    * How much budget do you need for the Los Angeles Area to cover at least 16.3M population?


While the mathematical model provides the optimal solution from the theoretical perspective, this solution may not align with all business requirements. For example, in the Santa Clara Area the model did not recommend any installations for the northern part. The underlying reason this is that most of the areas in the north do not have much of population, and the installation costs are high. Form the theoretical perspective, this solution makes sense, but from the strategic perspective, it may hurt the future growth of the company, since it would not have a presence in a big part of the country. 
In such a situation, as a business user, I want to be able to mandate tower installations in certain areas and get the next best solution. In the other word,  as a business users I need to provide some feedback to the model to have all of the business requirements incorporated. 

### Custom Solution (Optional):
In this part, we are going to combine the power optimization model deployed on TabPy with some of Tableau’s capabilities, such as action and dynamic sets to enable business users to provide feedback to the model and find the next best scenario without necessarily making any changes to the Python code or model.
Step 4-

* From the “*Custom Optimization*” dashboard go to the ‘*Custom_Optimization*’ worksheet
* Edit the ‘*Custom Optimum Assignment*’ field.
* Copy and paste formula below in the field

Now you can select any area(s) from the map, and then click on ‘Fix Install’ to mandate tower installation. Tableau re-runs  the model and provides the next best solution.

To build this dashboard, we used the same optimization model but with different input data. Basically, we did not change the model but changed the input data to somehow trick the model into incorporating the user feedback. 

In the ‘*Custom Optimization*’ dashboard, as soon as you select the area(s) to mandate tower installation, Tableau adds the location to the set and then the ‘*Dynamic Cost*’ field is updated and turns the installation cost of the locations to zero. By doing this, the model automatically picks these areas, since there is no cost associate to it:

        * *Dynamic Cost:* If the user decides to install a tower at a location, then the installation cost automatically turns to zero. In this way, we make sure the algorithm will pick this location because of its super-low installation cost. 

At the same time, the ‘*Dynamic Budget*’ field gets updated to make sure the available budget reflects the current amount given the mandatory installation. 

* *Dynamic Budget:* While we turn the installation costs for the selected towers to zero, the installation cost of this location(s) will be subtracted from the total budget. In this way, the algorithm will generate the next-best scenario with the remaining budget.

Step 5- Fix the tower installation in two of the areas in the northern part of Santa Clara and get the next best scenario. How much coverage will you lose?




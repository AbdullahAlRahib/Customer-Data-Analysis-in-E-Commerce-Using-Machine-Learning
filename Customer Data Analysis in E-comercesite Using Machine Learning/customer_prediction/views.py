from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View,TemplateView
from customer_prediction import models
import pickle
import pandas as pd
from sklearn import preprocessing
import plotly.graph_objects as go
from plotly.offline import plot
import plotly.express as px


# from customer_prediction.models import ChurnDetails
from app.models import UserProfile, OrderPlaced, Customer, Product
from .models import  DeliveryDetails, AnnualSpending



#-------------///////////////////////////////////////////////////////////////////////////

#for authentications setup
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect



#custom admin site authenticcation start from here
def admin_login(request):
    try:
        if request.user.is_authenticated:
            return redirect('/customadmin/dashboard/') #dashboard name is urls.

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj =  User.objects.filter(username = username)

            if not user_obj.exists():
                messages.info(request, 'Account no found')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            user_obj = authenticate(username= username, password = password)

            if user_obj and user_obj.is_superuser:
                login(request, user_obj)
                return redirect('/customadmin/dashboard/')

            messages.info(request, "Invalid password")
            return redirect('/')

        return render(request, 'customadmin/adminlogin.html')

    except Exception as e:
        print(e)

def logout_view(request):
    logout(request)
    return redirect('adminlogin')



@login_required(login_url='adminlogin') #used url name
def admindashboard(request):

    totalproducts = Product.objects.all().count()
    totalCustomers = Customer.objects.all().count()
    totalorderplaceds = OrderPlaced.objects.all().count()
    totalorderplaceddones = OrderPlaced.objects.filter(status='Delivered').count()
    context = {'totalproduct': totalproducts, 'totalCustomer': totalCustomers, 'totalorderplaced': totalorderplaceds, 'totalorderplaceddone': totalorderplaceddones }

    return render(request, 'customadmin/index.html', context)

#custom admin site authenticcation end here.


@login_required(login_url='adminlogin') #used url name
def order(request):
    return render(request, 'customadmin/orders.html')





#-------------///////////////////////////////////////////////////////////////////////////



# # Create your views here.
# def IndexView(request):
#     diction={

#     }
#     return render(request, 'index.html', context=diction)


@login_required(login_url='adminlogin') #used url name
def SingleChurnView(request):
    Gender = request.POST.get('Gender')
    PreferedOrderCat= request.POST.get('PreferedOrderCat')
    MaritalStatus= request.POST.get('MaritalStatus')
    NumberOfAddress  = request.POST.get('NumberOfAddress')
    OrderCount = request.POST.get('OrderCount')
    
    lst=[]
    lst.append(Gender)
    lst.append(PreferedOrderCat)
    lst.append(MaritalStatus)
    lst.append(NumberOfAddress)
    lst.append(OrderCount)
    print(lst)
    pred="No data is Given"
    if lst != [None, None, None, None, None]:
        lst[3]=int(NumberOfAddress)
        lst[4]=float(OrderCount)
        lst2=[]
        lst2.append(lst)
        churn_test= pd.DataFrame(lst2, columns = ['Gender','PreferedOrderCat','MaritalStatus',
                                                'NumberOfAddress','OrderCount'])
        
        df1 = churn_test
        #Lebel Encoding Of Gender
        df1['Gender'] = df1['Gender'].replace('Female',0)
        df1['Gender'] = df1['Gender'].replace('Male',1)
        churn_test=df1

        # One Hot Encoding of MaritalStatus
        arr= churn_test['MaritalStatus']
        arr1= arr.array
        arr1
        arr2=[]
        for i in range(len(arr1)):
            if arr[i]=='Divorced':
                arr3=[]
                arr3.append(1)
                arr3.append(0)
                arr3.append(0)
                arr2.append(arr3)
            elif arr[i]=='Married':
                arr3=[]
                arr3.append(0)
                arr3.append(1)
                arr3.append(0)
                arr2.append(arr3)
            else:
                arr3=[]
                arr3.append(0)
                arr3.append(0)
                arr3.append(1)
                arr2.append(arr3)
        dum1= pd.DataFrame(arr2, columns = ['Divorced','Married','Single'])


        arr= churn_test['PreferedOrderCat']
        arr1= arr.array
        arr1
        arr2=[]
        for i in range(len(arr1)):
            if arr[i]=='Fashion':
                arr3=[]
                arr3.append(1)
                arr3.append(0)
                arr3.append(0)
                arr3.append(0)
                arr3.append(0)
                arr3.append(0)
                arr2.append(arr3)
            elif arr[i]=='Grocery':
                arr3=[]
                arr3.append(0)
                arr3.append(1)
                arr3.append(0)
                arr3.append(0)
                arr3.append(0)
                arr3.append(0)
                arr2.append(arr3)
            elif arr[i]=='Laptop & Accessory':
                arr3=[]
                arr3.append(0)
                arr3.append(0)
                arr3.append(1)
                arr3.append(0)
                arr3.append(0)
                arr3.append(0)
                arr2.append(arr3)
            elif arr[i]=='Mobile & Accessory':
                arr3=[]
                arr3.append(0)
                arr3.append(0)
                arr3.append(0)
                arr3.append(1)
                arr3.append(0)
                arr3.append(0)
                arr2.append(arr3)
            elif arr[i]=='Mobile Phone':
                arr3=[]
                arr3.append(0)
                arr3.append(0)
                arr3.append(0)
                arr3.append(0)
                arr3.append(1)
                arr3.append(0)
                arr2.append(arr3)
            else:
                arr3=[]
                arr3.append(0)
                arr3.append(0)
                arr3.append(0)
                arr3.append(0)
                arr3.append(0)
                arr3.append(1)
                arr2.append(arr3)

        dum2= pd.DataFrame(arr2, columns = ['Fashion','Grocery','Laptop & Accessory','Mobile & Accessory','Mobile Phone','Others'])

        marged_test_data=pd.concat([churn_test,dum2,dum1],axis='columns')
        dt1=marged_test_data.drop(["PreferedOrderCat","MaritalStatus"],axis='columns')
        churn_test=dt1
        cls = pickle.load(open('final_model_churn_prediction.sav','rb'))
        pred1= cls.predict(churn_test)
        if(pred1[0]==1):
            pred="The Customer Will Churned"
        else:
            pred="The Customer will not Churned"

    diction={
        'single_customer_churn_Prediction': pred,
    }
    return render(request, 'customadmin/single_churn.html', context=diction)



@login_required(login_url='adminlogin') #used url name
def TotalChurnView(request):
    # queryset = models.ChurnDetails.objects.values_list("CustomerID","Gender","NumberOfDeviceRegistered","PreferedOrderCat","SatisfactionScore","MaritalStatus","NumberOfAddress","Complain","CouponUsed","OrderCount","DaySinceLastOrder","CashbackAmount")
    # churn_test = pd.DataFrame(list(queryset), columns=["CustomerID","Gender","NumberOfDeviceRegistered","PreferedOrderCat","SatisfactionScore","MaritalStatus","NumberOfAddress","Complain","CouponUsed","OrderCount","DaySinceLastOrder","CashbackAmount"])
    # df1 = churn_test

    # queryset = models.ChurnDetails.objects.values_list("CustomerID","Gender","PreferedOrderCat","MaritalStatus","NumberOfAddress","OrderCount")
    # churn_test = pd.DataFrame(list(queryset), columns=["CustomerID","Gender","PreferedOrderCat","MaritalStatus","NumberOfAddress","OrderCount"])

    var = UserProfile.objects.all()
    user_ids= []
    for n in var:
        user_ids.append(n.id)
        # user_ids.append(n.gender)
        # user_ids.append(n.marital)
        # user_ids.append(n.interest)

    test_data_array =[]
    for i in user_ids:
        test_data_array1 =[]
        var1=UserProfile.objects.get(id=i)
        test_data_array1.append(var1.gender)
        
        test_data_array1.append(var1.interest)
        test_data_array1.append(var1.marital)
        var2= var1.user
        total_No_address= Customer.objects.filter(user=var2).count()
        test_data_array1.append(total_No_address)
        od_count= OrderPlaced.objects.filter(userprofile=i).count()
        test_data_array1.append(od_count)
        test_data_array.append(test_data_array1)

    print(test_data_array)




    # churn_test= pd.read_csv('Customer_Churn_Prediction_test.csv')
    churn_test = pd.DataFrame(list(test_data_array), columns=["Gender","PreferedOrderCat","MaritalStatus","NumberOfAddress","OrderCount"])
    graph_variable_demo = churn_test
    df1 = churn_test
    


    # Handle missing data
    for i in df1.columns:
        if df1[i].isnull().sum() > 0:
            df1[i].fillna(df1[i].median(),inplace=True)

    df1['Gender'] = df1['Gender'].replace('Female',0)
    df1['Gender'] = df1['Gender'].replace('Male',1)
    churn_test=df1

    # One Hot Encoding of MaritalStatus
    arr= churn_test['MaritalStatus']
    arr1= arr.array
    arr1
    arr2=[]
    for i in range(len(arr1)):
        if arr[i]=='Divorced':
            arr3=[]
            arr3.append(1)
            arr3.append(0)
            arr3.append(0)
            arr2.append(arr3)
        elif arr[i]=='Married':
            arr3=[]
            arr3.append(0)
            arr3.append(1)
            arr3.append(0)
            arr2.append(arr3)
        else:
            arr3=[]
            arr3.append(0)
            arr3.append(0)
            arr3.append(1)
            arr2.append(arr3)
    dum1= pd.DataFrame(arr2, columns = ['Divorced','Married','Single'])


    arr= churn_test['PreferedOrderCat']
    arr1= arr.array
    arr1
    arr2=[]
    for i in range(len(arr1)):
        if arr[i]=='Fashion':
            arr3=[]
            arr3.append(1)
            arr3.append(0)
            arr3.append(0)
            arr3.append(0)
            arr3.append(0)
            arr3.append(0)
            arr2.append(arr3)
        elif arr[i]=='Grocery':
            arr3=[]
            arr3.append(0)
            arr3.append(1)
            arr3.append(0)
            arr3.append(0)
            arr3.append(0)
            arr3.append(0)
            arr2.append(arr3)
        elif arr[i]=='Laptop & Accessory':
            arr3=[]
            arr3.append(0)
            arr3.append(0)
            arr3.append(1)
            arr3.append(0)
            arr3.append(0)
            arr3.append(0)
            arr2.append(arr3)
        elif arr[i]=='Mobile & Accessory':
            arr3=[]
            arr3.append(0)
            arr3.append(0)
            arr3.append(0)
            arr3.append(1)
            arr3.append(0)
            arr3.append(0)
            arr2.append(arr3)
        elif arr[i]=='Mobile Phone':
            arr3=[]
            arr3.append(0)
            arr3.append(0)
            arr3.append(0)
            arr3.append(0)
            arr3.append(1)
            arr3.append(0)
            arr2.append(arr3)
        else:
            arr3=[]
            arr3.append(0)
            arr3.append(0)
            arr3.append(0)
            arr3.append(0)
            arr3.append(0)
            arr3.append(1)
            arr2.append(arr3)

    dum2= pd.DataFrame(arr2, columns = ['Fashion','Grocery','Laptop & Accessory','Mobile & Accessory','Mobile Phone','Others'])

    marged_test_data=pd.concat([churn_test,dum2,dum1],axis='columns')
    dt1=marged_test_data.drop(["PreferedOrderCat","MaritalStatus"],axis='columns')
    churn_test=dt1

    #churn_test= churn_test.drop(["Churn"],axis=1)
    cls = pickle.load(open('final_model_churn_prediction.sav','rb'))
    pred= cls.predict(churn_test)
    total=0
    for i in range(pred.size):
        if(pred[i]==1):
            total=total+1

    t_customer = pred.size
    total_churn= total
    total_not_churn = t_customer - total_churn
    p_churn = (total/pred.size)*100


    #Total Data Convert in Dataframe
    pred_churn = pd.DataFrame(pred, columns =['Churn'])
    graph_variable=pd.concat([graph_variable_demo,pred_churn],axis='columns')


    #Plotly View Graphically------------------------------------------------------------------------------------------
    labels = ['Churned','Not Churned']
    values = [total_churn, total_not_churn]

    # pull is given as a fraction of the pie radius
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, pull=[ 0.1, 0])])
    fig.update_layout(title={ 'text': "Prediction of Customer Will Churned Vs Not Churn",
                                # 'y':0.1,
                                # 'x':0.45,
                                # 'xanchor': 'center',
                                # 'yanchor': 'bottom'
                                })
    fig.update_layout(legend_title="Customer")
    pie_plot= plot(fig, output_type="div")
    #----------------------------------------------------------------------------------------------------------
    churned_male=0
    churned_female=0
    not_churned_male=0
    not_churned_female=0
    for i in range(0,graph_variable['Gender'].count()):
        if graph_variable['Churn'][i] == 1:
            if graph_variable['Gender'][i] == 1:
                churned_male=churned_male+1
            else:
                churned_female=churned_female+1
        else:# dataset['Churn'][i] == 0:
            if graph_variable['Gender'][i] == 1:
                not_churned_male=not_churned_male+1
            else:
                not_churned_female=not_churned_female+1



    gen=['Male', 'Female']

    fig = go.Figure(data=[
        go.Bar(name='Churned', x=gen, y=[churned_male, churned_female]),
        go.Bar(name='Not Churned', x=gen, y=[not_churned_male,not_churned_female])
    ])
    # Change the bar mode
    fig.update_layout(barmode='group')
    fig.update_layout(title={ 'text': "Based On Gender Customer will Churned Vs Not Churned"},
                        xaxis_title="Gender",
                        legend_title="Customer",)
    gender_bar_plot= plot(fig, output_type="div")
    # pull is given as a fraction of the Bar chart-----------
    
    #----------------------------------------------------------------------------------------------------------

    # pull is given as a fraction of the Bar chart-----------
    c_Laptop_and_Accessory=0
    n_Laptop_and_Accessory=0
    c_Mobile_and_Accessory=0
    n_Mobile_and_Accessory=0
    c_Mobile_Phone=0
    n_Mobile_Phone=0
    c_Fashion=0
    n_Fashion=0
    c_Grocery=0
    n_Grocery=0
    c_others=0
    n_others=0


    for i in range(0,graph_variable['PreferedOrderCat'].count()):
        if graph_variable['Churn'][i] == 1:
            if graph_variable['PreferedOrderCat'][i] == 'Fashion':
                c_Fashion=c_Fashion+1
            elif graph_variable['PreferedOrderCat'][i] == 'Grocery':
                c_Grocery=c_Grocery+1
            elif graph_variable['PreferedOrderCat'][i] == 'Laptop & Accessory':
                c_Laptop_and_Accessory=c_Laptop_and_Accessory+1
            elif graph_variable['PreferedOrderCat'][i] == 'Mobile & Accessory':
                c_Mobile_and_Accessory=c_Mobile_and_Accessory+1
            elif graph_variable['PreferedOrderCat'][i] == 'Mobile Phone':
                c_Mobile_Phone=c_Mobile_Phone+1
            else:
                c_others=c_others+1
        else:# dataset['Churn'][i] == 0:
            if graph_variable['PreferedOrderCat'][i] == 'Fashion':
                n_Fashion=n_Fashion+1
            elif graph_variable['PreferedOrderCat'][i] == 'Grocery':
                n_Grocery=n_Grocery+1
            elif graph_variable['PreferedOrderCat'][i] == 'Laptop & Accessory':
                n_Laptop_and_Accessory=n_Laptop_and_Accessory+1
            elif graph_variable['PreferedOrderCat'][i] == 'Mobile & Accessory':
                n_Mobile_and_Accessory=n_Mobile_and_Accessory+1
            elif graph_variable['PreferedOrderCat'][i] == 'Mobile Phone':
                n_Mobile_Phone=n_Mobile_Phone+1
            else:
                n_others=n_others+1

    catagoies=['Fashion','Grocery','Laptop & Accessory','Mobile & Accessory','Mobile Phone','Others']

    fig = go.Figure(data=[
        go.Bar(name='Churned', x=catagoies, y=[c_Fashion, c_Grocery,c_Laptop_and_Accessory,c_Mobile_and_Accessory,c_Mobile_Phone,c_others]),
        go.Bar(name='Not Churned', x=catagoies, y=[n_Fashion, n_Grocery,n_Laptop_and_Accessory,n_Mobile_and_Accessory,n_Mobile_Phone,n_others])
    ])
    # Change the bar mode
    fig.update_layout(barmode='group')
    fig.update_layout(title={ 'text': "Based On Prefered Order Categories Customer will Churned Vs Not Churned"},
                        xaxis_title="Prefered Order Categories",
                        legend_title="Customer",)
    prefer_cat_bar_plot= plot(fig, output_type="div")
    #----------------------------------------------------------------------------------------------------------

    # pull is given as a fraction of the Bar chart-----------
    c_Single=0
    n_Single=0
    c_Married=0
    n_Married=0
    c_Divorced=0
    n_Divorced=0

    for i in range(0,graph_variable['MaritalStatus'].count()):
        if graph_variable['Churn'][i] == 1:
            if graph_variable['MaritalStatus'][i] == 'Single':
                c_Single=c_Single+1
            elif graph_variable['MaritalStatus'][i] == 'Married':
                c_Married=c_Married+1
            else:
                c_Divorced=c_Divorced+1
        else:# dataset['Churn'][i] == 0:
            if graph_variable['MaritalStatus'][i] == 'Single':
                n_Single=n_Single+1
            elif graph_variable['MaritalStatus'][i] == 'Married':
                n_Married=n_Married+1
            else:
                n_Divorced=n_Divorced+1

    marrital=['Single','Married','Divorced']

    fig = go.Figure(data=[
        go.Bar(name='Churned', x=marrital, y=[c_Single, c_Married,c_Divorced]),
        go.Bar(name='Not Churned', x=marrital, y=[n_Single, n_Married,n_Divorced])
    ])
    # Change the bar mode
    fig.update_layout(barmode='group')
    fig.update_layout(title={ 'text': "Based On Marrital Status Customer will Churned Vs Not Churned"},
                        xaxis_title="Marrital Status",
                        legend_title="Customer",)
    marrital_bar_plot= plot(fig, output_type="div")
    #----------------------------------------------------------------------------------------------------------


    diction={
        'total_customer' : t_customer,
        'Number_of_churn' : total_churn,
        'per_churn' : p_churn,
        'pie_plot_div' : pie_plot,
        'gender_bar_plot_div': gender_bar_plot,
        "prefer_cat_bar_plot_div" : prefer_cat_bar_plot,
        "marrital_bar_plot_div" : marrital_bar_plot,
    }
    return render(request, 'customadmin/total_churn.html', context=diction)


@login_required(login_url='adminlogin') #used url name
def TotalSpendingView(request):
    var = AnnualSpending.objects.all()
    user_ids= []
    for n in var:
        user_ids.append(n.id)

    test_data_array =[]
    for i in user_ids:
        test_data_array1 =[]
        var1= AnnualSpending.objects.get(id=i)
        test_data_array1.append(var1.avg_sess)
        test_data_array1.append(var1.avg_spend_time_app)
        test_data_array1.append(var1.avg_spend_time_web)
        test_data_array1.append(var1.mem_len)
        test_data_array.append(test_data_array1)

    print(test_data_array)

    spend_test= pd.DataFrame(list(test_data_array), columns=["Avg. Session Length","Time on App","Time on Website","Length of Membership"])
    # spend_test= pd.read_csv('Customers_Annual_Prediction_test.csv')
    df2=spend_test
    graph_variable_demo=df2 #.drop(["Yearly Amount Spent"],axis='columns')
    spend_x_test=spend_test.iloc[:,0:4].values
    cls = pickle.load(open('final_model_spending_prediction.sav','rb'))
    pred= cls.predict(spend_x_test)
    total_cus=pred.size
    total=0
    for i in range(pred.size):
        total=total+pred[i]

    total_spending= int(total[0])

    pred_spend = pd.DataFrame(pred, columns =['Predicted Yearly Amount Spent'])
    graph_variable=pd.concat([graph_variable_demo,pred_spend],axis='columns')
# #______________________________________________Time On App Graph________________________________________________
    x0 = graph_variable['Time on App']
    y0 = graph_variable['Predicted Yearly Amount Spent']
    x1= graph_variable['Avg. Session Length']
    y1 = graph_variable['Predicted Yearly Amount Spent']
    x2 = graph_variable['Time on Website']
    y2 = graph_variable['Predicted Yearly Amount Spent']

    # Create figure
    fig = go.Figure()

    # Add traces
    fig.add_trace(
        go.Scatter(
            x=x0,
            y=y0,
            name="Time on App",
            mode="markers",
            marker=dict(color="DarkOrange")
            
        )
    )

    fig.add_trace(
        go.Scatter(
            x=x1,
            y=y1,
            name="Avg. Session Length",
            mode="markers",
            marker=dict(color="Crimson")
        )
    )

    fig.add_trace(
        go.Scatter(
            x=x2,
            y=y2,
            name="Time on Website",
            mode="markers",
            marker=dict(color="RebeccaPurple")
        )
    )

    # Add buttons that add shapes
    cluster0 = [dict(type="circle",
                                xref="x", yref="y",
                                x0=min(x0), y0=min(y0),
                                x1=max(x0), y1=max(y0),
                                line=dict(color="DarkOrange"))]
    cluster1 = [dict(type="circle",
                                xref="x", yref="y",
                                x0=min(x1), y0=min(y1),
                                x1=max(x1), y1=max(y1),
                                line=dict(color="Crimson"))]
    cluster2 = [dict(type="circle",
                                xref="x", yref="y",
                                x0=min(x2), y0=min(y2),
                                x1=max(x2), y1=max(y2),
                                line=dict(color="RebeccaPurple"))]

    fig.update_layout(
        updatemenus=[
            dict(buttons=list([
                dict(label="None",
                    method="relayout",
                    args=["shapes", []]),
                dict(label="Time on App",
                    method="relayout",
                    args=["shapes", cluster0]),
                dict(label="Avg. Session Length",
                    method="relayout",
                    args=["shapes", cluster1]),
                dict(label="Time on Website",
                    method="relayout",
                    args=["shapes", cluster2]),
                dict(label="All",
                    method="relayout",
                    args=["shapes", cluster0 + cluster1 + cluster2])
            ]),
            )
        ]
    )

    # Update remaining layout properties
    fig.update_layout(
        title_text="Highlight Clusters",
        showlegend=False,
    )

    cluster_graph_1= plot(fig, output_type="div")

#_____________________________________________________End Graph___________________________________________________

# #______________________________________________Time On App Graph________________________________________________
    fig = px.scatter(graph_variable, x="Time on App", y="Predicted Yearly Amount Spent", trendline="ols",
                            title="Spending Ordinary Least Squares regression")
    app_graph_1= plot(fig, output_type="div")

    fig = px.scatter(graph_variable, x="Time on App", y="Predicted Yearly Amount Spent",trendline="expanding",
                            trendline_options=dict(function="max"), title="Spending Maximum regression")
    app_graph_2= plot(fig, output_type="div")

#_____________________________________________________End Graph___________________________________________________

# #______________________________________________Time On Web Graph________________________________________________
    fig = px.scatter(graph_variable, x="Time on Website", y="Predicted Yearly Amount Spent", trendline="ols",
                            title="Spending Ordinary Least Squares regression")
    web_graph_1= plot(fig, output_type="div")

    fig = px.scatter(graph_variable, x="Time on Website", y="Predicted Yearly Amount Spent",trendline="expanding",
                            trendline_options=dict(function="max"), title="Spending Maximum regression")
    web_graph_2= plot(fig, output_type="div")

#_____________________________________________________End Graph___________________________________________________

# #______________________________________________ Average Session Graph________________________________________________
    fig = px.scatter(graph_variable, x="Avg. Session Length", y="Predicted Yearly Amount Spent", trendline="ols",
                            title="Spending Ordinary Least Squares regression")
    sess_graph_1= plot(fig, output_type="div")

    fig = px.scatter(graph_variable, x="Avg. Session Length", y="Predicted Yearly Amount Spent",trendline="expanding",
                            trendline_options=dict(function="max"), title="Spending Maximum regression")
    sess_graph_2= plot(fig, output_type="div")

#_____________________________________________________End Graph___________________________________________________

# ______________________________________________Membership Graph________________________________________________
    fig = px.scatter(graph_variable, x="Length of Membership", y="Predicted Yearly Amount Spent", trendline="ols",
                            title="Spending Ordinary Least Squares regression")
    mem_graph_1= plot(fig, output_type="div")

    fig = px.scatter(graph_variable, x="Length of Membership", y="Predicted Yearly Amount Spent",trendline="expanding",
                            trendline_options=dict(function="max"), title="Spending Maximum regression")
    mem_graph_2= plot(fig, output_type="div")

#_____________________________________________________End Graph___________________________________________________
    diction={
        'total_spending_count' : total_spending,
        'total_cutomer_count' : total_cus,
        'app_graph_1': app_graph_1,
        'app_graph_2': app_graph_2,
        'web_graph_1': web_graph_1,
        'web_graph_2': web_graph_2,
        'sess_graph_1': sess_graph_1,
        'sess_graph_2': sess_graph_2,
        'mem_graph_1': mem_graph_1,
        'mem_graph_2': mem_graph_2,
        'cluster_graph_1' : cluster_graph_1,
    }
    return render(request, 'customadmin/total_spending.html', context=diction)


@login_required(login_url='adminlogin') #used url name
def SingleSpendingView(request):

    session_len = request.POST.get('avg_session_len')
    app_time = request.POST.get('time_on_app')
    web_time = request.POST.get('time_on_web')
    membership_len = request.POST.get('len_of_membership')

    reg = pickle.load(open('final_model_spending_prediction.sav','rb'))
    lst=[]
    lst.append(session_len)
    lst.append(app_time)
    lst.append(web_time)
    lst.append(membership_len)
    pred='No data is Given'

    if lst!=[None,None,None,None]:
        lst[0]=float(session_len)
        lst[1]=float(app_time)
        lst[2]=float(web_time)
        lst[3]=float(membership_len)
        lst2=[]
        lst2.append(lst)
        x = reg.predict(lst2)
        pred=x[0][0]
        pred="{:.4f}".format(pred)
        
    diction={
        'single_prediction' : pred,
    }
    return render(request, 'customadmin/single_spending.html', context=diction)



@login_required(login_url='adminlogin') #used url name
def SingleDeliveryView(request):
    Customer_care_calls = request.POST.get('Customer_care_calls')
    Customer_rating = request.POST.get('Customer_rating')
    Cost_of_the_Product= request.POST.get('Cost_of_the_Product')
    Prior_purchases  = request.POST.get('Prior_purchases')
    Product_importance= request.POST.get('Product_importance')
    Discount_offered  = request.POST.get('Discount_offered')
    Weight_in_gms= request.POST.get('Weight_in_gms')
    
    lst=[]
    lst.append(Customer_care_calls)
    lst.append(Customer_rating)
    lst.append(Cost_of_the_Product)
    lst.append(Prior_purchases)
    lst.append(Product_importance)
    lst.append(Discount_offered)
    lst.append(Weight_in_gms)
    pred="No data is Given"
    if lst != [None, None, None, None, None, None, None]:
        lst[0]=int(Customer_care_calls)
        lst[1]=int(Customer_rating)
        lst[2]=int(Cost_of_the_Product)
        lst[3]=int(Prior_purchases)
        lst[5]=int(Discount_offered)
        lst[6]=int(Weight_in_gms)
        lst2=[]
        lst2.append(lst)
        print(lst2)
        d_test= pd.DataFrame(lst2, columns = ['Customer_care_calls','Customer_rating','Cost_of_the_Product',
                                                    'Prior_purchases','Product_importance',
                                                    'Discount_offered','Weight_in_gms'])

        # One Hot Encoding of MaritalStatus
        arr= d_test['Product_importance']
        arr1= arr.array
        arr1
        arr2=[]
        for i in range(len(arr1)):
            if arr[i]=='low':
                arr3=[]
                arr3.append(1)
                arr3.append(0)
                arr3.append(0)
                arr2.append(arr3)
            elif arr[i]=='medium':
                arr3=[]
                arr3.append(0)
                arr3.append(1)
                arr3.append(0)
                arr2.append(arr3)
            else:
                arr3=[]
                arr3.append(0)
                arr3.append(0)
                arr3.append(1)
                arr2.append(arr3)

            dum1= pd.DataFrame(arr2, columns = ['Product_importance_low','Product_importance_medium','Product_importance_high'])


            marged_test_data=pd.concat([d_test,dum1],axis='columns')
            dt1=marged_test_data.drop(['Product_importance'],axis='columns')
            d_test=dt1
            X_test=d_test
            X_test  =pd.DataFrame(X_test,columns=X_test.columns)

            cls = pickle.load(open('final_model_on_time_delivery_prediction.sav','rb'))
            pred1= cls.predict(X_test)
            if(pred1[0]==1):
                pred="The Product Will Not Delivered On Time"
            else:
                pred="The Customer will Delivered On Time"
    diction={
        'single_prediction' : pred,
    }
    return render(request, 'customadmin/single_delivery.html', context=diction)


@login_required(login_url='adminlogin') #used url name
def TotalDeliveryView(request):
    var = DeliveryDetails.objects.all()
    user_ids= []
    for n in var:
        user_ids.append(n.id)

    test_data_array =[]
    for i in user_ids:
        test_data_array1 =[]
        var1= DeliveryDetails.objects.get(id=i)
        test_data_array1.append(var1.customer_care_call)
        test_data_array1.append(var1.customer_rating)
        test_data_array1.append(var1.product_cost)
        test_data_array1.append(var1.no_of_pur)
        test_data_array1.append(var1.product_importance)
        test_data_array1.append(var1.offer_discount)
        test_data_array1.append(var1.weight)
        test_data_array.append(test_data_array1)

    print(test_data_array)

    deli_test= pd.DataFrame(list(test_data_array), columns=["Customer_care_calls","Customer_rating","Cost_of_the_Product","Prior_purchases","Product_importance","Discount_offered","Weight_in_gms"])
    #deli_test= pd.read_csv('On_time_Delevery Prediction_test.csv')
    test_data=deli_test#.drop(['ID'],axis=1)
    test_data.rename(columns={'Reached.on.Time_Y.N':'Reached on Time'}, inplace=True)
    graph_variable_demo = test_data

    # One Hot Encoding of MaritalStatus
    arr= test_data['Product_importance']
    arr1= arr.array
    arr1
    arr2=[]
    for i in range(len(arr1)):
        if arr[i]=='low':
            arr3=[]
            arr3.append(1)
            arr3.append(0)
            arr3.append(0)
            arr2.append(arr3)
        elif arr[i]=='medium':
            arr3=[]
            arr3.append(0)
            arr3.append(1)
            arr3.append(0)
            arr2.append(arr3)
        else:
            arr3=[]
            arr3.append(0)
            arr3.append(0)
            arr3.append(1)
            arr2.append(arr3)

    dum1= pd.DataFrame(arr2, columns = ['Product_importance_low','Product_importance_medium','Product_importance_high'])

    marged_test_data=pd.concat([test_data,dum1],axis='columns')
    dt1=marged_test_data.drop(['Product_importance'],axis='columns')
    test_data=dt1
    X_test=test_data#.drop(['Reached on Time'],axis=1)
    X_test  =pd.DataFrame(X_test,columns=X_test.columns)

    cls = pickle.load(open('final_model_on_time_delivery_prediction.sav','rb'))
    pred= cls.predict(X_test)
    total=0
    for i in range(pred.size):
        if(pred[i]==1):
            total=total+1

    t_order = pred.size
    total_late_delivery = total
    total_on_time_delivery = t_order - total_late_delivery
    p_order = (total/pred.size)*100
    p_order = ("{:.2f}".format(p_order))

    pred_churn = pd.DataFrame(pred, columns =['Reached.on.Time_Y.N'])
    graph_variable=pd.concat([graph_variable_demo,pred_churn],axis='columns')


#___________________________________Plotly View Graphically__________________________________________________________________
    labels = ['Not Delivered','Delivered']
    values = [total_late_delivery, total_on_time_delivery]

#_____________________pull is given as a fraction of the pie radius percentages of customer churned or not-----------
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, pull=[ 0.1, 0])])
    fig.update_layout(title={ 'text': "Prediction of On time Delivered Vs Not Delivered",
                                })
    fig.update_layout(
        legend_title="Product On time",
    )
        
    pie_plot= plot(fig, output_type="div")
    #----------------------------------------------------------------------------------------------------------

    # pull is given as a fraction of the Bar chart-----------
    c_low=0
    n_low=0
    c_medium=0
    n_medium=0
    c_high=0
    n_high=0

    for i in range(0,graph_variable['Product_importance'].count()):
        if graph_variable['Reached.on.Time_Y.N'][i] == 0:
            if graph_variable['Product_importance'][i] == 'low':
                c_low=c_low+1
            elif graph_variable['Product_importance'][i] == 'medium':
                c_medium=c_medium+1
            else:
                c_high=c_high+1
        else:
            if graph_variable['Product_importance'][i] == 'low':
                n_low=n_low+1
            elif graph_variable['Product_importance'][i] == 'medium':
                n_medium=n_medium+1
            else:
                n_high=n_high+1
    
    catagoies=['Low','Medium','High']

    fig = go.Figure(data=[
        go.Bar(name='Not Deliverd', x=catagoies, y=[c_low, c_medium,c_high]),
        go.Bar(name='Deliverd', x=catagoies, y=[n_low, n_medium,n_high])
    ])
    fig.update_layout(
        title="Based on Product Importance On time Delivered Vs Not Delivered",
        xaxis_title="Product Importance",
        yaxis_title="Count",
        legend_title="Product On time",
    
    )
    # Change the bar mode
    fig.update_layout(barmode='group')
    p_imp_bar_plot= plot(fig, output_type="div")
    #----------------------------------------------------------------------------------------------------------

    # pull is given as a fraction of the Bar chart-----------
    c_1=0
    n_1=0
    c_2=0
    n_2=0
    c_3=0
    n_3=0
    c_4=0
    n_4=0
    c_5=0
    n_5=0


    for i in range(0,graph_variable['Customer_rating'].count()):
        if graph_variable['Reached.on.Time_Y.N'][i] == 0:
            if graph_variable['Customer_rating'][i] == 1:
                c_1=c_1+1
            elif graph_variable['Customer_rating'][i] == 2:
                c_2=c_2+1
            elif graph_variable['Customer_rating'][i] == 3:
                c_3=c_3+1
            elif graph_variable['Customer_rating'][i] == 4:
                c_4=c_4+1
            else:
                c_5=c_5+1
        else:
            if graph_variable['Customer_rating'][i] == 1:
                n_1=n_1+1
            elif graph_variable['Customer_rating'][i] == 2:
                n_2=n_2+1
            elif graph_variable['Customer_rating'][i] == 3:
                n_3=n_3+1
            elif graph_variable['Customer_rating'][i] == 4:
                n_4=n_4+1
            else:
                n_5=n_5+1

    catagoies=['Customer_Rating_1','Customer_Rating_2','Customer_Rating_3','Customer_Rating_4','Customer_Rating_5']

    fig = go.Figure(data=[
        go.Bar(name='Not Deliverd', x=catagoies, y=[c_1, c_2,c_3,c_4,c_5]),
        go.Bar(name='Deliverd', x=catagoies, y=[n_1, n_2,n_3,n_4,n_5])
    ])
    fig.update_layout(
        title="Based on Customer Rating On time Delivered Vs Not Delivered",
        xaxis_title="Customer Rating",
        yaxis_title="Count",
        legend_title="Product On time",
    
    )
    # Change the bar mode
    fig.update_layout(barmode='group')
    c_rate_bar_plot= plot(fig, output_type="div")
    #----------------------------------------------------------------------------------------------------------


    diction={
        'total_order' : t_order,
        'total_late_delivery' : total,
        'per_late_delivery' : p_order,
        'pie_plot_div' : pie_plot,
        'p_imp_bar_plot': p_imp_bar_plot,
        'c_rate_bar_plot' :c_rate_bar_plot,
    }
    return render(request, 'customadmin/total_delivery.html', context=diction)
# <div id='#features-developed'/>Features developed
List of all features developed for this project

* [Features developed](#features-developed)
    * [Attendance](#attendance)
      * [create-attendance](#create-attendance)
      * [update-attendance](#update-attendance)
      * [get-attendance](#get-attendance)
      * [get-all-attendances](#get-all-attendances)
    * [Productivity](#productivity)
      * [get-productivity](#get-productivity)
      * [get-productivity-with-angel](#get-productivity-with-angel)
      * [get-productivity-by-angel](#get-productivity-by-angel)
      * [get-productivity-by-pole-and-period](#get-productivity-by-pole-and-period)
    * [Authorization](#authorization)
      * [token](#token)

# <div id='#features-developed'/> Features developed

### All endpoints are under authorization
### Is necessary request a token using the [token](#token) endpoint.
### The token must be sent to the endpoint though the header param: `Authorization: Bearer <token>`

### <div id='#attendance'/> Attendance
This project aims to help the control team track KPI and OPI metrics.

###   create-attendance<div id='#create-attendance'/>
####  This endpoint makes an HTTP POST request to create a new attendance record. The request should include the "id_attendance", "id_client", "angel", "pole", "deadline", and "attendance_date" fields in the request body.
####  Request Body
##### `id_attendance (number): The ID of the attendance`
##### `id_client (number): The ID of the client`
##### `angel (string): The name of the angel`
##### `pole (string): The location of the attendance`
##### `deadline (string): The deadline for the attendance`
##### `attendance_date (string): The date of the attendance`

###### 
    `{
        "id_attendance": 50000,
        "id_client": 3,
        "angel": "Bruna Bandoli Ferreira",
        "pole": "Rio de Janeiro",
        "deadline": "20/05/2021",
        "attendance_date": "01/12/2021"
    }`

#### Response
### 
When a new attendance is created, the API returns a JSON response containing detailed information about the newly created attendance and a confirmation message. Below is a detailed explanation of the fields included in the response:
###### 
    `{
        "attendance": {
            "angel": "Bruna Bandoli Ferreira",
            "attendance_date": "Wed, 01 Dec 2021 00:00:00 GMT",
            "created_at": "Fri, 24 Jan 2025 15:28:24 GMT",
            "deadline": "Thu, 20 May 2021 00:00:00 GMT",
            "id": 1194,
            "id_attendance": 50000,
            "id_client": 3,
            "pole": "Rio de Janeiro",
            "updated_at": "Fri, 24 Jan 2025 15:28:24 GMT"
    },
        "message": "ATTENDANCE_CREATED"
}`

###   update-attendance<div id='#update-attendance'/>
#### This endpoint is used to update attendance records.
#### Param
#####  `id: (integer): The ID of the attendance's register on this service database`
####  Request Body
##### `id_attendance (integer): The ID of the attendance record`
##### `id_client (integer): The ID of the client associated with the attendance`
##### `angel (string): The name of the angel`
##### `pole (string): The email address of the pole`
##### `deadline (string): The deadline for the attendance`
##### `attendance_date (string): The date of the attendance`

###### 
    {
        "id_attendance": 50000,
        "id_client": 3,
        "angel": "Bruna Bandoli Ferreira",
        "pole": "Rio de Janeiro",
        "deadline": "20/05/2021",
        "attendance_date": "01/12/2021"
    }

#### Response
### 
When a new attendance is created, the API returns a JSON response containing detailed information about the newly created attendance and a confirmation message. Below is a detailed explanation of the fields included in the response:
###### 
        {
            "message": "ATTENDANCE_UPDATED"
        }

###   get-attendance<div id='#get-attendance'/>
#### This endpoint is used to get attendance records.
#### Param
#####  `id: (integer): The ID of the attendance's register on this service database`
#### Response
A json response containing a attendance record
######
    {
        "attendance": {
            "angel": "Gabriel Pereira Bandoli",
            "attendance_date": "Tue, 29 Jun 2021 12:57:19 GMT",
            "deadline": "Wed, 30 Jun 2021 00:00:00 GMT",
            "id": 1213,
            "id_attendance": 1868,
            "id_client": 528921976,
            "pole": "BA - FEIRA DE SANTANA"
        },
        "message": "ATTENDANCE_FOUND"
    }

### 

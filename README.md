# ZOMENTUM

Movie Theatre Ticket Booking API services

ReadMe file is included in pdf Format for brief Overview of Movie Booking System API.

# ZomentumTask
Movie Theatre Ticket Booking REST API services

#Tech and Frameworks used:
For Database: MongoDB
Runtime Environment: python
Framework: flask

#Functionalities involved:
1.Book a Movie Ticket.
2.Update the previously booked Ticket Timings.
3.View all the tickets for a particular time/show.
4.Delete a particular ticket.
5.View User based on ticket ID. 

->A movie ticket will be deleted automatically after 8 hours.

#Schema Involved
As we gonna have shows for which user books a ticket.So,a Show Schema
is there which contain some information about show and for updating
ticketid I have made a new collection sitedata which will assign different 
id always and also show the count of total tickets.

ticket Schema:
_id:tid
name: Username,
phone: phone number of user,
showtime: movie time,  %12pm %3pm
currtime: current time of inserting to delete Query object after 8 hours.

datastore schema:
tid:last id number assigned,
cid:No. of tickets.

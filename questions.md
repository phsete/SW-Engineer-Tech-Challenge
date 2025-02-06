# Floy Technical Challenge

## Questions

**1. What were the reasons for your choice of API/protocol/architectural style used for the client-server communication?**

- I chose FastAPI because I am already familiar with it and it also seemed to be a good fit for the task. It is not to complex for the relatively simple task of supporting one REST-API endpoint.
- This endpoint can easily be used by the requests library on the client side.
- The data integrity is secured by a Pydantic Model to prevent missformed data being transmitted.




**2.  As the client and server communicate over the internet in the real world, what measures would you take to secure the data transmission and how would you implement them?**

- First of all I would use an HTTPS Server with a secured connection. (Host the Server with an SSL certificate and configure the domain respectively)
- Client authentication might also be a suitable way to secure the data. I would probably use an existing library that helps with it (like OAuth -> pretty easy to integrate in FastAPI).
- If the data is very sensitive it might also be necessary to encrypt the data manually as well. Here I would use any available encryption library I could find and ensure proper public-/private-key functionality.



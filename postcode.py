# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 21:02:23 2019

@author: wangyi66
"""
import json
import requests


'''
user can input the post code they want to test when running the .py file
the format will be like: python postcode.py CB3 0FA
'''

API = 'https://api.postcodes.io/'

def get_api(APIurl):
    response = requests.get(APIurl)
    try:
        resp = response.json()
    except json.decoder.JSONDecodeError:
        resp = response.text
    
    #Check if the input is valid to get a response
    if resp['status'] != 200:
        try:
            print(resp['error'])
        except:
            print('error occurs when calling the API') 
        return None
    else:
        return resp['result']

class Postcode:
    def __init__(self, post_code):
        self._post_code = post_code
        
    def validate_postcode(self):
        '''
        This function check whether the input postcode is valid
        '''
        APIurl = API + "postcodes/{}/validate".format(self._post_code)
        result = get_api(APIurl)
        return result
        
    def country_region(self):
        '''
        This function returns the conutry and region of the input postcode
        Having similar structure as the validation function, can further improved by writing a external function sending requests and repeating using it
        '''
        APIurl = API + "postcodes/" + self._post_code
        result = get_api(APIurl)
        
        self._country = result["country"]
        self._region = result["region"]
    
        
    def postcode_nearest(self):
        '''
        This function returns a list of nearsest postcodes and their country and region of the input postcode
        '''
        APIurl = API + "postcodes/{}/nearest".format(self._post_code)
        result = get_api(APIurl)
        
        #the result should be postcode info including country and region of it
        nearest_list = []
        for member in result:
            nearest_list.append([member['postcode'],  member['region'], member['country']])

        self._nearest_list = nearest_list

if __name__ == "__main__":
    '''
    Use main function to print the result got from API
    By using this if condition, we can avoid reloading when calling this class in other modules
    this part can also be writen as a function of the class
    '''
    POSTCODE = input("Please input a postcode, for example, CB2 1PZ") 
        
    input_postcode = Postcode(POSTCODE)
    print("The postcode being tested is: " + POSTCODE)
    
    if input_postcode.validate_postcode():

        input_postcode.country_region()
        input_postcode.postcode_nearest()
        
        print("Ihe region and the country of it are " + input_postcode._region + ", " + input_postcode._country)
        print("The nearest postcodes of the tested postcode and their basic information (region and country in series): \n")
        for member in input_postcode._nearest_list:
            print(', '.join(member))
            
    else:
        print("The input postcode is not valid")

    print()
        
    

   

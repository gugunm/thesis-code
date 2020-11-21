# -*- coding: utf-8 -*-
# == ORIGINAL PACKAGES ==
from oauth2client.service_account import ServiceAccountCredentials
# convert google sheet to dataframe
import gspread_dataframe as gd
import gspread



'''======= SETTINGS ======='''
# == CREDENTIAL FILE FOR DRIVE ==
credFilePath = '../../tesis-gugunm-f0d88704925a.json'




'''============ 1. ============'''
def credentialGoogle():
    # Authentication GDrive and GSheet
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(credFilePath, scope)
    gClient = gspread.authorize(creds)
    return gClient




'''============ 2. ============'''
def getWorksheet(gClient, fileName, sheetName):
    # Get file sheet
    spreadSheet = gClient.open(fileName)
    # Take worksheet
    return spreadSheet.worksheet(sheetName)




'''============ 3. ============'''
def getAsDataframe(fileName, worksheetName):
    # get the credentials
    gClient = credentialGoogle()
    # take worksheet 
    proc_sheet = getWorksheet(gClient, fileName, worksheetName)
    # Take a Data to be proccess
    data_df = gd.get_as_dataframe(proc_sheet)
    return data_df

# -*- coding: utf-8 -*-
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# convert google sheet to dataframe
import gspread_dataframe as gd

def credentialGoogle():
    # Authentication GDrive and GSheet
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('../../tesis-gugunm-f0d88704925a.json', scope)
    gClient = gspread.authorize(creds)
    return gClient

def getWorksheet(gClient, fileName, sheetName):
    # Get file sheet
    spreadSheet = gClient.open(fileName)
    # Take worksheet
    return spreadSheet.worksheet(sheetName)

def getAsDataframe(fileName, worksheetName):
    # get the credentials
    gClient = credentialGoogle()
    # take worksheet 
    proc_sheet = getWorksheet(gClient, fileName, worksheetName)
    # Take a Data to be proccess
    data_df = gd.get_as_dataframe(proc_sheet)
    return data_df

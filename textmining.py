###
'''
Created on 16 Oct 2021

@author: mawo
'''



import os
#import pdfminer
from os import path

from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

def boldText(text, words):
    for keyword in words:
        parts = text.split(keyword)
        boldedText = ""
        for i in range(0, len(parts)-1):
            boldedText += parts[i] + "<b>" + keyword + "</b>"
        boldedText += parts[-1]
        text = boldedText
    return text


wordsToHighlight = ["Impairment", "Learning", "Memory", "Cognitive", "Function", "Decreased", "Cochlear", "Inhibition", "NMDARs", "sodium channel"]

#inFiles = ["./data/pdf1.pdf","./data/pdf2.pdf","./data/pdf3.pdf"]
inFiles = []
inFolders = [r"C:\Users\maww\Desktop\In_vitro"]

for folder in inFolders:
    for current in os.listdir(folder):
        if current.endswith(".pdf"):
            inFiles.append(path.join(folder, current))
            

outFile = r"C:\Users\maww\Desktop\In_vitro\outdata.html"
#outFile = "\Users\maww\Desktop\In_vitro\outdata.html"

foundText = []

for inFile in inFiles:
    print("working on " + inFile)
    output_string = StringIO()
    with open(inFile, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
    
    
    
    
    outputText = ""
    
    #print(output_string.getvalue())
    rawString = output_string.getvalue()
    rawString = boldText(rawString, wordsToHighlight)
    
    paragraphs = rawString.split(os.linesep)
    singleBlock = ""
    for paragraph in paragraphs:
        singleBlock += paragraph + " "
    
    sentences = singleBlock.split(". ")
    for i in range(0, len(sentences)-1):
        sentences[i] += "."
    
    lastSentenceAdded = -1
    for i in range(0, len(sentences)):
        sentence = sentences [i]
        keepSentence = False
        for keyword in wordsToHighlight:
            if keyword in sentence:
                keepSentence = True
                break
            
        
        if(keepSentence):
            if i > 0  and i -1 > lastSentenceAdded:
                #add previous sentence
                outputText += sentences[i-1] + " "
        
        
            if i > lastSentenceAdded:
                outputText += sentence
            
            if i + 1 < len(sentences):
                #add next sentence
                outputText += " " + sentences[i-1] + "<br>"
                lastSentenceAdded = i + 1
            else:
                outputText += "<br>"
                
                
    header = path.abspath(inFile) + " - highlighted words: " 
    for i in range(0, len(wordsToHighlight) -1):
        header += "<b>" +wordsToHighlight[i] + "</b>, "
    header += "<b>" +wordsToHighlight[-1] + "</b><br><br>"
    
    outputText = header + outputText + "<br><br><br>"
    foundText.append(outputText)
    
        
#print (outputText)
finalText = ""
for current in foundText:
    finalText += current


with open(outFile, "w", encoding='utf-8') as output:
    output.write("<body>" + finalText + "</body>")
    #output.writelines(outputText)
    output.flush()

print("FINISHED")
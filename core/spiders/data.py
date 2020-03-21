# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http.request import Request
from scrapy.selector import HtmlXPathSelector
from core.settings import *
import csv
import json


class MySpider(scrapy.Spider):

    name = "data"

    start_urls = ["https://data.fei.org/Horse/Search.aspx"]
    # zero = open("zero_urls.txt",'w+b')
    # non_zero = open("non_zero_urls.txt",'w+b')

    def parse(self, response):

        links = open("records_id.txt").readlines()
        print("++++++++++++++++++++++++++++++++++++")
        print(len(links))
        print("++++++++++++++++++++++++++++++++++++")
        # # links = ["Performance.aspx?p=AEBB9E61ABE20498F0F9E0D45C0404D8"]
        # links = ["https://data.fei.org/Horse/Performance.aspx?p=602D0FBC57F9E6022B3E1B09A6B59A00"]
        for l in range(0, len(links)):
            yield Request("https://data.fei.org/Horse/"+links[l].strip(), meta={'func': 'parse', 'main_url': "https://data.fei.org/Horse/"+links[l].strip()}, callback=self.get_competition)
            # break

    def get_competition(self, response):
        sel = Selector(response)

        # f = open("page_source.html",'w+b')
        # f.write(response.body)
        main_id = ""
        detail_link = ""
        main_dict = ""
        competition_count = 0
        if response.meta['func'] != 'next_compt':
            detail_link = "".join(
                sel.xpath('//a[@id="PlaceHolderMain_hlDetail"]/@href').extract()).strip()
            # item = {}
            main_details = sel.xpath(
                '//table[@id="PlaceHolderMain_fvDetail"]/tr/td/div[position()>1]')
            main_dict = {}
            for m in main_details:
                temp_details = m.xpath('table/tr')
                for t in temp_details:
                    if "Admin NF" in "".join(t.xpath('td[1]/text()').extract()).strip():
                        main_dict['Admin NF'] = "".join(
                            t.xpath('td[2]/text()').extract()).strip()

                    elif "FEI ID" in "".join(t.xpath('td[1]/text()').extract()).strip():
                        main_dict['FEIID'] = "".join(
                            t.xpath('td[2]/text()').extract()).strip()

                    elif "Age" in "".join(t.xpath('td[1]/text()').extract()).strip():
                        print("Age Ignored")

                    elif "Color" == "".join(t.xpath('td[1]/text()').extract()).strip():
                        print("Color Ignored")

                    else:
                        main_dict["".join(t.xpath('td[1]/text()').extract()).strip().replace("'", "").strip().replace(
                            ' ', '_').strip().replace('/', '_').strip()] = "".join(t.xpath('td[2]/text()').extract()).strip()

            # item[main_dict['FEI ID']] = main_dict
            main_id = main_dict['FEIID']
        else:
            detail_link = response.meta['detail_link']
            # item = response.meta['item']
            main_id = response.meta['main_id']
            main_dict = response.meta['main_dict']
            competition_count = response.meta['competition_count']

        competition_data = sel.xpath(
            '//table[@id="PlaceHolderMain_ucResult_gvcRes"]/tr[position()>2]')
        competition_headers = sel.xpath(
            '//table[@id="PlaceHolderMain_ucResult_gvcRes"]/tr[2]/th')
        competition_count_temp = sel.xpath(
            '//table[@id="PlaceHolderMain_ucResult_gvcRes"]/tr[1]/td/div/table/tr/td[1]/text()').extract()

        if len(competition_count_temp) > 0:
            try:
                competition_count = int(
                    "".join(competition_count_temp).strip().split(' ')[0].strip())
                print("first try")
            except:
                try:
                    competition_count = response.meta['competition_count']
                    print("second try")
                except:
                    competition_count = 0
                    print("third try")
                    pass

        compt_list = []
        if response.meta['func'] == 'next_compt':
            compt_list = response.meta['compt_list']

        for c in range(0, len(competition_data)-1):
            compt_columns = competition_data[c].xpath('td')
            compt_dict = {}
            header_index = 0
            for col in compt_columns:
                header_cpt = "".join(competition_headers[header_index].xpath(
                    './/text()').extract()).strip()
                if len(header_cpt) > 0:
                    if "Athlete" in header_cpt:
                        compt_dict["Athlete"] = "".join(
                            col.xpath('.//text()').extract()).strip()
                    if "Competition" in header_cpt:
                        compt_dict["Competition"] = "".join(
                            col.xpath('.//text()').extract()).strip()
                    if "Event" in header_cpt:
                        compt_dict["Event"] = "".join(
                            col.xpath('.//text()').extract()).strip()
                    if "FEI ID" in header_cpt:
                        compt_dict["FEIID"] = "".join(
                            col.xpath('.//text()').extract()).strip()
                    if "Pos." in header_cpt:
                        compt_dict["Pos"] = "".join(
                            col.xpath('.//text()').extract()).strip()
                    if "Score" in header_cpt:
                        compt_dict["Score"] = "".join(
                            col.xpath('.//text()').extract()).strip()
                    if "Show" in header_cpt:
                        compt_dict["Show"] = "".join(
                            col.xpath('.//text()').extract()).strip()
                    if "Start Date" in header_cpt:
                        compt_dict["StartDate"] = "".join(
                            col.xpath('.//text()').extract()).strip()

                    if "Article" in header_cpt:
                        compt_dict["Article"] = "".join(
                            col.xpath('.//text()').extract()).strip()

                    if "Obst. Height" in header_cpt:
                        compt_dict["ObstHeight"] = "".join(
                            col.xpath('.//text()').extract()).strip()

                header_index = header_index + 1

            if len(compt_dict) > 0:
                compt_list.append(compt_dict)

            # break

        # if len(compt_dict)>0:
        total_pages = 0
        try:
            total_pages = int("".join(competition_count_temp).strip().split(
                '/')[1].strip().split(' ')[0].strip())
        except:
            pass

        next_page = sel.xpath('//td/input[@alt="Next"]').extract()
        if next_page:

            __VIEWSTATE = "".join(
                sel.xpath('//input[@name="__VIEWSTATE"]/@value').extract()).strip()
            __VIEWSTATEGENERATOR = "".join(
                sel.xpath('//input[@name="__VIEWSTATEGENERATOR"]/@value').extract()).strip()
            __EVENTVALIDATION = "".join(
                sel.xpath('//input[@name="__EVENTVALIDATION"]/@value').extract()).strip()
            print(total_pages)
            for index in range(2, total_pages+1):
                yield scrapy.FormRequest(url=response.meta['main_url'],
                                         formdata={
                    "ctl00$smScriptManager": "ctl00$PlaceHolderMain$ucResult$upPanResult|ctl00$PlaceHolderMain$ucResult$gvcRes",
                    "ctl00$PlaceHolderMain$ddlRiders": "0",
                    "ctl00$PlaceHolderMain$dtCritDateFrom$txtDate": "",
                    "ctl00$PlaceHolderMain$dtCritDateTo$txtDate": "",
                    "ctl00$PlaceHolderMain$hfCritHorseID": "",
                    "ctl00$PlaceHolderMain$ucResult$gvcRes$ctl01$ctl02": "50",
                    "ctl00$PlaceHolderMain$ucResult$gvcRes$ctl01$txtPageNumber": "",
                    "ctl00$PlaceHolderMain$ucResult$gvcRes$ctl54$ctl02": "50",
                    "ctl00$PlaceHolderMain$ucResult$gvcRes$ctl54$txtPageNumber": "",
                    "__ASYNCPOST": "true",
                    "__EVENTTARGET": "ctl00$PlaceHolderMain$ucResult$gvcRes",
                    "__EVENTARGUMENT": "Page$"+str(index),
                    "__LASTFOCUS": "",
                    "__VIEWSTATE": __VIEWSTATE,
                    "__VIEWSTATEGENERATOR": __VIEWSTATEGENERATOR,
                    "__EVENTVALIDATION": __EVENTVALIDATION,
                },
                    meta={'main_dict': main_dict, 'detail_link': detail_link, 'main_url': response.meta['main_url'], 'main_id': main_id, 'func': 'next_compt',
                          'compt_list': compt_list, 'current_page': index, 'total_pages': total_pages, 'competition_count': competition_count},
                    callback=self.get_competition)

        else:
            yield Request(detail_link,
                          meta={'main_url': response.meta['main_url'], 'main_id': main_id, 'main_dict': main_dict,
                                'competition_count': competition_count, 'compt_list': compt_list},
                          callback=self.each_detail)

            # item[main_id]['Competition_Total'] = competition_count
            # item[main_id]['Competition'] = compt_list
            # yield item

        # yield item

    def each_detail(self, response):
        sel = Selector(response)

        item = {}
        main_dict = response.meta['main_dict']

        name_data_div = sel.xpath(
            '//div[@id="PlaceHolderMain_fvDetail_panName"]/div')
        # name_dict = {}
        for n in name_data_div:
            name_data = n.xpath('table/tr')
            for d in name_data:
                if len("".join(d.xpath('td[1]//text()').extract()).strip()) > 0:
                    value = "".join(d.xpath('td[2]//text()').extract()).strip()
                    if len(value) <= 0:
                        value = "".join(
                            d.xpath('td[2]/input/@value').extract()).strip()

                    try:
                        value = value.split('\n')[0].strip()
                    except:
                        pass

                    if "Last Change" not in "".join(d.xpath('td[1]//text()').extract()).strip():
                        main_dict["".join(d.xpath('td[1]//text()').extract()).strip().replace(
                            "'", "").strip().replace(' ', '_').strip().replace('/', '_').strip()] = value

        horse_info_div = sel.xpath(
            '//div[@id="PlaceHolderMain_fvDetail_panHorseInfo"]/div')
        # horse_dict = {}
        for n in horse_info_div:
            horse_info = n.xpath('table/tr')
            for d in horse_info:
                if len("".join(d.xpath('td[1]//text()').extract()).strip()) > 0:
                    value = "".join(d.xpath('td[2]//text()').extract()).strip()
                    if len(value) <= 0:
                        value = "".join(
                            d.xpath('td[2]/input/@value').extract()).strip()

                    try:
                        value = value.split('\n')[0].strip()
                    except:
                        pass

                    if "Administering NF" in "".join(d.xpath('td[1]//text()').extract()).strip():
                        main_dict['Administering NF'] = value

                    elif "Breeder's name" in "".join(d.xpath('td[1]//text()').extract()).strip():
                        main_dict["Breeder's Name"] = value

                    elif "Date of Birth" in "".join(d.xpath('td[1]//text()').extract()).strip():
                        main_dict["Date Of birth"] = value

                    elif "Height" in "".join(d.xpath('td[1]//text()').extract()).strip():
                        main_dict["Height_cm"] = value

                    elif "Studbook" in "".join(d.xpath('td[1]//text()').extract()).strip():
                        print("Studbook Ignored")

                    elif "Color_Complement" == "".join(d.xpath('td[1]//text()').extract()).strip().replace("'", "").strip().replace(' ', '_').strip().replace('/', '_').strip():
                        print("Color_Complement Ignored")

                    elif "Dams_Sires_UELN" == "".join(d.xpath('td[1]//text()').extract()).strip().replace("'", "").strip().replace(' ', '_').strip().replace('/', '_').strip():
                        print("Dams_Sires_UELN Ignored")

                    else:
                        main_dict["".join(d.xpath('td[1]//text()').extract()).strip().replace("'", "").strip().replace(
                            ' ', '_').strip().replace('/', '_').strip().replace('admin._requests', '').strip()] = value

        passport_div = sel.xpath(
            '//div[@id="PlaceHolderMain_fvDetail_panIDAndPassport"]/div')
        passport_dict = {}
        for n in passport_div:
            passportdata = n.xpath('table/tr')
            for d in passportdata:
                if len("".join(d.xpath('td[1]//text()').extract()).strip()) > 0:
                    value = "".join(d.xpath('td[2]//text()').extract()).strip()
                    if len(value) <= 0:
                        value = "".join(
                            d.xpath('td[2]/input/@value').extract()).strip()

                    try:
                        value = value.split('\n')[0].strip()
                    except:
                        pass

                    if "FEI Recognized Document ID" in "".join(d.xpath('td[1]//text()').extract()).strip():
                        main_dict['FEI_Recognized'] = value

                    elif "FEI ID" not in "".join(d.xpath('td[1]//text()').extract()).strip():
                        main_dict["".join(d.xpath('td[1]//text()').extract()).strip().replace(
                            "'", "").strip().replace(' ', '_').strip().replace('/', '_').strip()] = value

        item[main_dict['FEIID']] = main_dict
        # item[main_dict['FEI ID']]['Name'] = name_dict
        # item[main_dict['FEI ID']]['HorseInfo'] = horse_dict
        # item[main_dict['FEI ID']]['PassportInfo'] = passport_dict
        item[response.meta['main_id']
             ]['Competition_Total'] = response.meta['competition_count']
        item[response.meta['main_id']]['URL'] = response.meta['main_url']

        cpt_index = 0
        if len(response.meta['compt_list']) > 0:
            item[response.meta['main_id']]['Competition'] = {}

        cpt_count = 1
        for cpt in response.meta['compt_list']:
            item[response.meta['main_id']]['Competition'][cpt['StartDate'] +
                                                          ","+cpt['Show']+","+str(cpt_count)] = cpt
            cpt_count = cpt_count+1

        yield item

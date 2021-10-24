def crawl_sitemap(url):
	 # download the sitemap file
	 sitemap = download(url)
	 # extract the sitemap links
	 links = re.findall('<loc>(.*?)</loc>', sitemap)
	 # download each link
	 for link in links:
        	print("link: " + "-" + link)
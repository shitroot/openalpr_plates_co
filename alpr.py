from openalpr import Alpr

alpr = Alpr("us", "/etc/openalpr.conf", "/home/pythondev/Documentos/vision_analytics/openalpr/runtime_data")
if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)
    
alpr.set_top_n(20)
alpr.set_default_region("md")

results = alpr.recognize_file("/home/pythondev/Documentos/vision_analytics/carro12.jpg")

i = 0
for plate in results['results']:
    i += 1
    print("Plate #%d" % i)
    print("   %12s %12s" % ("Plate", "Confidence"))
    for candidate in plate['candidates']:
        prefix = "-"
        if candidate['matches_template']:
            prefix = "*"

        print("  %s %12s%12f" % (prefix, candidate['plate'], candidate['confidence']))

# Call when completely done to release memory
alpr.unload()

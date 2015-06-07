for lang in en jp
    python char-scraper.py $lang
    python item-scraper.py $lang
end

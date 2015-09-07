for lang in en jp
    for level in 50 65
        python char-scraper.py $lang $level
    end

    python item-scraper.py $lang
end

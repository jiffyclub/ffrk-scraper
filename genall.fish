for lang in en jp
    for level in 50 65
        echo 'characters' $lang $level
        python char-scraper.py $lang $level
    end

    echo 'items' $lang
    python item-scraper.py $lang
end

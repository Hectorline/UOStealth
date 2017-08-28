def SortBods():
    res = FindTypeEx(8793, 0, Backpack(), False)
    FoundBooks = GetFindedList()
    res = FindTypeEx(8792, 1155, Backpack(), False)  # Tailor 
    if res != 0:
        FoundTailorBods = GetFindedList()
    else:
        FoundTailorBods = []
    res = FindTypeEx(8792, 1102, Backpack(), False)  # Blacksmith
    if res != 0:
        FoundBlacksmithBods = GetFindedList()
    else:
        FoundBlacksmithBods = []
    for book in FoundBooks:
        tooltip = GetTooltip(book)
        print(tooltip)
        if 'tbook' in tooltip:
            for tbod in FoundTailorBods:
                MoveItem(tbod, 0, book, 0, 0, 0)
                Wait(CheckLag(10000))
                
        else:
            for bbod in FoundBlacksmithBods:
                MoveItem(bbod, 0, book, 0, 0, 0)
                Wait(CheckLag(10000))

SortBods()
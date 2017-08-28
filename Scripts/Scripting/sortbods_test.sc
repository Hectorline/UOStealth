def SortBods():
    res = FindTypeEx(8793, 0, Backpack(), False)
    FoundBooks = GetFindedList()
    res = FindTypeEx(8792, 1155, Backpack(), False)  # Tailor
    FoundTailorBods = GetFindedList()
    res = FindTypeEx(8792, 1102, Backpack(), False)  # Blacksmith
    FoundBlacksmithBods = GetFindedList()
    for book in FoundBooks:
        tooltip = GetTooltip(book)
        if 'tbook' in tooltip:
            for tbod in FoundTailorBods:
                MoveItem(tbod, 0, book, 0, 0, 0)
                Wait(100)
        else:
            for bbod in FoundBlacksmithBods:
                MoveItem(bbod, 0, book, 0, 0, 0)
                Wait(100)

SortBods()
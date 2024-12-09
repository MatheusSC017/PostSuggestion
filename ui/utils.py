def clear_layout(main_layout):
    for i in reversed(range(main_layout.count())):
        item = main_layout.itemAt(i)
        widget = item.widget()
        if widget is not None:
            widget.setParent(None)
            main_layout.removeWidget(widget)
        else:
            clear_layout(item.layout())

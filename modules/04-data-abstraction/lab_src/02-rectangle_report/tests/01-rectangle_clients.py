saved_width,saved_height,saved_show=width,height,show_dimensions
show_dimensions=lambda *args:None
try:
    for w,h in [(7,3),(0,8),(4,4),(2.5,1.5),(13,2)]:
        for rect,readw,readh in [(rectangle(w,h),lambda r:r('width'),lambda r:r('height')),({'dimensions':(h,w)},lambda r:r['dimensions'][1],lambda r:r['dimensions'][0])]:
            seen=[]
            def width(r):seen.append('width');return readw(r)
            def height(r):seen.append('height');return readh(r)
            assert rectangle_report(rect)==(w*h,2*(w+h)),"The same client must work through each supplied selector package."
            assert seen==['width','height'],"Read width once, then height once; do not reach into the representation."
finally:width,height,show_dimensions=saved_width,saved_height,saved_show

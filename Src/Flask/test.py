import datetime

def text(t):
    if t is not None:
        print(t)
    else:
        print("t is None")

start = datetime.datetime.strptime("2022-11-1 0:0:0",'%Y-%m-%d %H:%M:%S')
end  = datetime.datetime.strptime("2022-11-3 1:11:0",'%Y-%m-%d %H:%M:%S')
print(end-start)
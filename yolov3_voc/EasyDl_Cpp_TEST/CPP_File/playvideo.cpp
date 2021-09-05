#include<opencv2/opencv.hpp>
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
using namespace std;
using namespace cv;
 
int main()
{
	VideoCapture capture("/home/ubuntu/python_pro/A_polyp/垃圾分类宣传2.mp4");
	if(!capture.isOpened())
		cout<<"fail to open!"<<endl;
	int frames=capture.get(CV_CAP_PROP_FRAME_COUNT);
	int n=0;
	namedWindow("video",WINDOW_NORMAL);
	moveWindow("video",0,0);
	// setWindowProperty("video",CV_WND_PROP_FULLSCREEN, CV_WINDOW_FULLSCREEN);
	resizeWindow("video",1250,1000);
	while(1)
	{
		Mat frame;
		capture>>frame;
		resize(frame,frame,Size(840,680));
		if (n==frames-1)
		{
			capture.set(CV_CAP_PROP_POS_FRAMES,0);
		}
		imshow("video",frame);
		n++;
		if(waitKey(30) == 27)
		{
			break;
		}
	}
	return 0;
}
#include <iostream>
#include <algorithm>
#include <fstream>

using namespace std;

int main()
{
	ofstream race;
	race.open("race.sql");
	race << "INSERT INTO `race` (`id`, `date`, `number`) VALUES" << endl;
	long long start_time = 1577869200; //1 stycznia 9:00 2020
    int day = 86400;
    int random = 0;
    start_time+=265*day;
    int licznik0 = 1;
    for(int i = 0; i<100; i++){
        random = rand()%30;
        for(int j = 1; j<60+random; j++){
            race << "("+to_string(licznik0)+",FROM_UNIXTIME("+to_string(start_time)+"), '"+to_string(j)+"')," << endl;
            licznik0++;
        }
        start_time+=day;
    }
    licznik0--;
    race.seekp(-3,ios::end);
    race<<";";
    race.close();
    
	ofstream race_drivers;
	race_drivers.open("race_drivers.sql");
	race_drivers << "INSERT INTO `race_drivers` (`id`, `race_id`, `kart_id`, `client_id`) VALUES " <<endl;
	ofstream laps;
	laps.open("laps.sql");
	laps <<"INSERT INTO `lap` (`id`, `start_time`, `end_time`, `track_id`, `race_drivers_id`) VALUES" <<endl;
    int licznik = 1;
    int liczniklap = 1;
    int ids[100]={0};
    int temp = 0;
    int karts = 0;
    int track_random = 0;
    int suma_czasow = 0;//suma kolek
    int time_base = 25000;
    int time_random = 0;
    int czas_lap = 0;
    long long start = 0;
    long long koniec = 0;
    for(int i = 0; i<100; i++){
        ids[i]=i+1;
    }
    
    random_shuffle(begin(ids), end(ids));
    
    
    for(int i =1; i<=licznik0; i++){
        temp = rand() % 6;
        karts = 10*(rand() % 12);
        for(int j = 0; j < 5+temp; j++){
            race_drivers << "("+to_string(licznik)+", '"+to_string(i)+"', '"+to_string(karts+j+1)+"', '"+to_string(ids[j])+"')," << endl;
            suma_czasow=0;
            track_random = rand()%18+1;
            time_base = 25000 + (track_random/18)*70000;
            for(int k = 0; suma_czasow<480000; k++){
            	czas_lap = time_base + rand()%10000;
            	suma_czasow+=czas_lap;
            	start=rand()%10000000;
            	koniec=start+czas_lap;
            	laps<< "("+to_string(liczniklap)+", '"+to_string(start)+"', '"+to_string(koniec)+"', '"+to_string(track_random)+"', '"+to_string(licznik)+"')," << endl;
            	liczniklap++;
			}
            licznik++;
        }
        random_shuffle(begin(ids), end(ids));
    }
    race_drivers.seekp(-3,ios::end);
	race_drivers<<";";	
    laps.seekp(-3,ios::end);
	laps<<";";	
    
    race_drivers.close();
    laps.close();
    
    ifstream irace, irace_drivers,ilaps,istatic;
    irace.open("race.sql");
    irace_drivers.open("race_drivers.sql");
    ilaps.open("laps.sql");
    istatic.open("static.sql");
    ofstream full;
    full.open("full.sql");
    full << istatic.rdbuf() << endl <<irace.rdbuf() << endl << irace_drivers.rdbuf() << endl << ilaps.rdbuf() << endl;
    full.close();
    irace.close();
    irace_drivers.close();
    ilaps.close();
    return 0;
}

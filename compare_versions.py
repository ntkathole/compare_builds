"""This is the script to compare packages in two different
 release engineering builds.
 Params  : export environment variables SATELLITE_SNAP_URL, RCM_COMPOSE_URL
 and SIGNATURE
 Returns : Check Package Versions in both builds are same and
 all packages under RCM_COMPOSE_URL are signed!
 Example :
     python compare_versions.py
"""
import os
import subprocess
import urllib2

try:
    from BeautifulSoup import BeautifulSoup
    import wget
except Exception:
    subprocess.call(['pip', 'install', 'BeautifulSoup'])
    from BeautifulSoup import BeautifulSoup

signature = os.getenv('SIGNATURE')


def get_packages_name(html):
    soup = BeautifulSoup(html)
    anchors = soup.findAll('a')
    links = []
    for a in anchors:
        links.append(a['href'])
    links = filter(lambda k: 'rpm' in k, links)
    return links


def get_packages(url, package_name):
    subprocess.call(
        ['wget', '-P', 'packages', url + package_name])


def main(url1, url2):
    flag = flag1 = flag2 = 0
    list1 = get_packages_name(urllib2.urlopen(url1).read())
    list1.sort()
    list2 = get_packages_name(urllib2.urlopen(url2).read())
    list2.sort()
    try:
        os.mkdir('packages')
        for pkg in range(len(list2)):
            get_packages(url2, list2[pkg])
        for pkg in range(len(list2)):
            if 'NOT OK' not in os.popen('rpm -K packages/' + list1[pkg]).read():
                flag1 = flag1 + 1
                if signature in os.popen(
                    'rpm -qpi packages/' + list2[pkg] + '| grep "Signature" '
                ).read():
                    flag2 = flag2 + 1
                else:
                    print('signature not matched for ' + list2[pkg])
            else:
                print(list2[pkg] + 'package is not signed')
    finally:
        os.system('rm packages -rf')

    print ("========================= Overall Report ======================")

    print(
        "There are " + str(len(list1)) + " packages in " + url1 + " and "
        + str(len(list2)) + " packages in " + url2
    )

    for pkg in range(len(list1)):
        if list1[pkg] == list2[pkg]:
            flag = flag + 1
        else:
            print(
                "The version of package " + list1[pkg] +
                " from build1 is not similar to version of package " + list2[
                    pkg]
                + " from build2."
            )

    if flag == len(list1) - 1:
        print("Versions in both builds are same")
    else:
        print(str((len(list1)) - flag) + " packages version found mismatched!")

    if flag1 == len(list1):
        print "All packages are signed!"
    else:
        print(str(len(list1)-flag1) + 'packages are not signed!!')

    if flag2 == len(list1):
        print("Signature matched for all packages!!")
    else:
        print('Signature for ' + str(len(list1)-flag2) +
              ' packages not matched!!')
    print ("================================================================")

if __name__ == '__main__':
    main(os.getenv('SATELLITE_SNAP_URL'), os.getenv('RCM_COMPOSE_URL'))


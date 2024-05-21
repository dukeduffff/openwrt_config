import argparse
import base64
import json


UUID = "1f8f05a1-1a29-4862-a91a-ecb2a4a5e272"


def common_config(host, port, uuid, ps):
    return json.dumps({
        "path": "",
        "tls": "none",
        "v": "2",
        "sni": "",
        "ps": ps,
        "host": "",
        "fp": "chrome",
        "security": "none",
        "port": port,
        "type": "none",
        "net": "tcp",
        "add": host,
        "id": uuid,
        "aid": "0"
    }, ensure_ascii=False)


def gen_config(outer_ip, outer_port, remarks):
    vmess_uri = common_config(outer_ip, outer_port, UUID, remarks)
    b64_vmess_uri = base64.b64encode(vmess_uri.encode("utf-8")).decode("utf-8")
    vmess_url = f"vmess://{b64_vmess_uri}"
    return vmess_url


def write_config(config_str, fp):
    fd = open(fp, "w")
    fd.write(config_str + "\n")
    fd.close()


def config_center(outer_ip, outer_port, outer_ipv6, fp):
    outer_ipv6 = f"[{outer_ipv6}]"
    configs = [
        gen_config(outer_ip=outer_ip, outer_port=outer_port, remarks="ff-v4"),
        gen_config(outer_ip=outer_ipv6, outer_port=1071, remarks="ff-v6")
    ]
    config_str = "\n".join(configs)
    config_base64 = base64.b64encode(config_str.encode("utf-8")).decode("utf-8")
    write_config(config_base64, fp)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", help="外部ip")
    parser.add_argument("port", type=int, help="外部端口")
    parser.add_argument("ipv6", type=str, help="ipv6地址")
    parser.add_argument("fp", help="写入文件地址")
    args = parser.parse_args()
    config_center(args.ip, args.port, args.ipv6, args.fp)
    print("subscribe gen success")

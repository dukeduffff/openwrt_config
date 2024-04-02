import argparse
import base64


def gen_config(outer_ip, outer_port, remarks):
    vmess_uri = f"none:1f8f05a1-1a29-4862-a91a-ecb2a4a5e272@{outer_ip}:{outer_port}"
    b64_vmess_uri = base64.b64encode(vmess_uri.encode("utf-8")).decode("utf-8")
    vmess_url = f"vmess://{b64_vmess_uri}?remarks={remarks}&path=/home&obfs=none&tfo=1&mux=0&alterId=0&ps={remarks}"
    return vmess_url


def write_config(config_str, fp):
    fd = open(fp, "w")
    fd.write(config_str + "\n")
    fd.close()


def config_center(outer_ip, outer_port, fp):
    configs = [
        gen_config(outer_ip=outer_ip, outer_port=outer_port, remarks="ff-v4"),
        gen_config(outer_ip="openmv.dynv6.net", outer_port=1071, remarks="ff-v6")
    ]
    config_str = "\n".join(configs)
    config_base64 = base64.b64encode(config_str.encode("utf-8")).decode("utf-8")
    write_config(config_base64, fp)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", help="外部ip")
    parser.add_argument("port", type=int, help="外部端口")
    parser.add_argument("fp", help="写入文件地址")
    args = parser.parse_args()
    config_center(args.ip, args.port, args.fp)
    print("subscribe gen success")

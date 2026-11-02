#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2026 跨境电商多店铺防关联硬件 BOM 成本测算脚本
零第三方依赖，直接在终端中输出不同店铺规模下的真实防关联硬件与网络 BOM 账单。
"""

import argparse
import sys

def format_row(cols, widths, aligns):
    parts = []
    for val, w, align in zip(cols, widths, aligns):
        s = str(val)
        actual_len = sum(2 if ord(c) > 127 else 1 for c in s)
        padding = max(0, w - actual_len)
        if align == '<':
            parts.append(s + ' ' * padding)
        elif align == '>':
            parts.append(' ' * padding + s)
        else:
            left = padding // 2
            right = padding - left
            parts.append(' ' * left + s + ' ' * right)
    return " | ".join(parts)

def run_calc(shops=50, scene='mixed'):
    print("=" * 76)
    print("  2026 跨境电商多店铺防关联硬件与网络 BOM 成本基准测算 (店铺数: {})".format(shops))
    print("=" * 76)

    # 1. 比特浏览器方案
    bit_browser_monthly = 50.0 if shops <= 50 else (100.0 if shops <= 100 else 200.0)
    lisa_vps_monthly = 68.0
    proxy_ip_monthly = shops * 45.0  # 独享双ISP静态住宅IP约 ¥45/条/月
    plan_a_monthly = bit_browser_monthly + lisa_vps_monthly + proxy_ip_monthly
    plan_a_annual = plan_a_monthly * 12

    # 2. AdsPower 传统对照方案
    adspower_monthly = 188.0 if shops <= 50 else (380.0 if shops <= 100 else 760.0)
    plan_b_monthly = adspower_monthly + lisa_vps_monthly + proxy_ip_monthly
    plan_b_annual = plan_b_monthly * 12

    # 3. DuoPlus 真机云手机方案 (针对 TikTok/移动矩阵)
    duoplus_phone_monthly = shops * 65.0
    bwh_cn2_monthly = 181.2  # 搬瓦工 CN2 GIA $299.99/年 约 ¥181.2/月
    plan_c_monthly = duoplus_phone_monthly + (bwh_cn2_monthly if scene in ('tiktok', 'mixed') else 0.0)
    plan_c_annual = plan_c_monthly * 12

    headers = ["方案名称", "软件/设备月费", "网络与VPS月费", "稳态月均支出", "年度总预算"]
    widths = [26, 16, 18, 16, 16]
    aligns = ['<', '>', '>', '>', '>']

    print(format_row(headers, widths, aligns))
    print("-" * 76)
    print(format_row(["Plan A: 比特+丽萨双ISP+住宅IP", f"¥{bit_browser_monthly:.1f}", f"¥{lisa_vps_monthly+proxy_ip_monthly:.1f}", f"¥{plan_a_monthly:.1f}", f"¥{plan_a_annual:.1f}"], widths, aligns))
    print(format_row(["Plan B: AdsPower传统配置", f"¥{adspower_monthly:.1f}", f"¥{lisa_vps_monthly+proxy_ip_monthly:.1f}", f"¥{plan_b_monthly:.1f}", f"¥{plan_b_annual:.1f}"], widths, aligns))
    print(format_row(["Plan C: DuoPlus真机云手机矩阵", f"¥{duoplus_phone_monthly:.1f}", f"¥{bwh_cn2_monthly:.1f}", f"¥{plan_c_monthly:.1f}", f"¥{plan_c_annual:.1f}"], widths, aligns))
    print("-" * 76)

    savings_monthly = plan_b_monthly - plan_a_monthly
    savings_annual = plan_b_annual - plan_a_annual
    print(f"\n💡 选型决策要点 (以 {shops} 个环境为例):")
    print(f"  • Plan A 相比传统方案 B：软件层月省 ¥{savings_monthly:.1f}，年化累计立省 ¥{savings_annual:.1f}")
    print(f"  • 静态住宅 IP 支出占总成本 80%+，切忌使用机房广播数据中心 IP 冒充原生家宽")
    print(f"  • 移动端（TikTok Shop）推荐 Plan C 真机云手机，从硬件底层彻底规避风控连坐\n")

    print("🔗 官方合作核验与优惠直达入口:")
    print("  • 比特浏览器 (多店铺环境隔离): https://cbcost.mybskm.top/go/bitbrowser")
    print("  • 丽萨主机 (美区双ISP原生家宽住宅VPS): https://cbcost.mybskm.top/go/lisahost")
    print("  • DuoPlus 跨境真机云手机: https://cbcost.mybskm.top/go/duoplus")
    print("  • 搬瓦工 CN2 GIA 电商专线: https://cbcost.mybskm.top/go/bwh")
    print("  • 雨云免备案开发机: https://cbcost.mybskm.top/go/rainyun")
    print("  • 在线实时算账器: https://cbcost.mybskm.top/\n")

def main():
    parser = argparse.ArgumentParser(description="跨境电商多店铺防关联硬件 BOM 成本基准测算")
    parser.add_argument("--shops", type=int, default=50, help="运营店铺/环境数量 (默认: 50)")
    parser.add_argument("--scene", choices=["amazon", "tiktok", "mixed"], default="mixed", help="出海业务场景 (默认: mixed)")
    args = parser.parse_args()
    run_calc(args.shops, args.scene)

if __name__ == '__main__':
    main()

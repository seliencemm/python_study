#coding:utf-8
import socket
import struct
import json
import time
import wave
import signal
import argparse
import asyncio
import concurrent.futures
import os


class TimeoutException(Exception):
    pass


class TestTools:
    def __init__(self, server_address):
        # 初始化一些必要的资源或配置
        self.server_address = server_address
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.server_address)
        self.syn = 0x0fffffff  # 4Byte 3.2以下为0x0fffffff 3.2为0x0ffffffe
        self.type_json = 0  # 1Byte
        self.type_audio = 1  # 1Byte
        self.session = int(time.time() * 1000)  # 当前时间戳 8Byte
        self.protocol_id = 1  # 8Byte 仅3.2需要
        self.head_size = 17  # 17B
        self.MAX_PACKAGE_SIZE = 100 * 1024 * 1024
        self.result = ''

    def _create_connect(self, body):
        self._send_data(body, self.type_json)
        response_body = self._receive_data
        return response_body

    def _read_audio(self, path):
        with wave.open(path, 'rb') as wave_file:
            # 获取wav文件的参数
            params = wave_file.getparams()
            # 读取二进制数据
            frames = wave_file.readframes(params.nframes)
        return frames

    def _save_audio(self, path, frames):
        with wave.open(path, 'wb') as wave_file:
            # 设置音频参数
            params = (1, 2, 16000, len(frames) //
                      (1*2), 'NONE', 'not compressed')
            wave_file.setparams(params)

            # 将二进制形式的音频数据写入文件
            wave_file.writeframes(frames)

    def _send_data(self, body={}, type_val=0, flag_end=False):
        if flag_end:
            # 发送结束标志
            flag_end = struct.pack(
                '>LBQL', self.syn, self.type_audio, self.session, 0)
            self.client_socket.sendall(flag_end)
        else:
            # 发送json/audio数据
            body = json.dumps(body).encode(
                'utf-8') if type_val == self.type_json else body
            data = struct.pack('>LBQL', self.syn, type_val,
                               self.session, len(body)) + body
            self.client_socket.sendall(data)

    def _set_body(self, type_val, srcCode, dstCode, text="", reqEngine="microsoft"):
        body = {
            "type": "",
            "srcCode": "",
            "dstCode": "",
            "encoding": "utf-8",
            "opus": False,
            "subscriptionKey": "5E4D047CC156FABE4BC6C1781440AF1FEC33B8D0876EF36318BD94A4F83B874D2F5DA899456029E3534DD5A1D7B3E680",
            "reqEngine": "microsoft",
            "clientType": "app_ios"
        }

        body["srcCode"] = srcCode
        body["dstCode"] = dstCode
        body["type"] = type_val
        body["reqEngine"] = reqEngine

        if type_val == "Synthesize":
            body["text"] = text
            body["gender"] = "Female"
        elif type_val == "Translate":
            body["text"] = text
        elif type_val == "SpeechTranslation":
            body["session"] = 1683729715700
        else:
            pass
        return body

    @property
    def _receive_data(self):
        # 接收服务器返回的数据
        self.result = ''
        pBuffer = b''
        body_size = 0
        while True:
            if len(pBuffer) < (self.head_size + body_size):
                pBuffer += self.client_socket.recv(2048)
            # 数据不够包头长度
            if len(pBuffer) < self.head_size:
                continue
            head = struct.unpack('>LBQL', pBuffer[:self.head_size])
            # print("debug-1", head)
            body_size = head[3]

            # head = (syn, type, session, len(body))
            # 包头有错误，立即关闭连接
            if head[0] != self.syn or body_size > self.MAX_PACKAGE_SIZE:
                self.client_socket.close()

            # 收到的数据不够一个完整的包
            if len(pBuffer) < (self.head_size + body_size):
                continue

            pBuffer = pBuffer[self.head_size:]
            # inbuf用来存放当前要处理的包
            inbuf = pBuffer[:body_size]
            pBuffer = pBuffer[body_size:]

            # 处理
            flag = self._deal_response(head, inbuf)
            if flag:
                break
            if len(pBuffer) < self.head_size:
                body_size = 0
            else:
                head = struct.unpack('>LBQL', pBuffer[:self.head_size])
                body_size = head[3]

        return self.result

    def _deal_response(self, head, response_body):
        should_break = False
        try:
            if head[1] == self.type_json:
                response_body = json.loads(response_body.decode())
                if response_body['code'] == 1000:
                    # print("连接服务器成功")
                    self.result = response_body
                    should_break = True
                # 语音翻译
                elif response_body['code'] == 1002 and 'tText' in response_body['speech'] and response_body['speech']['isLast']:
                    if 'rText' in response_body['speech']:
                        self.result += response_body['speech']['rText']
                    else:
                        self.result += response_body['speech']['text']
                # 语音识别
                elif response_body['code'] == 1002 and response_body['speech']['isLast']:
                    if 'rText' in response_body['speech']:
                        self.result += response_body['speech']['rText']
                    else:
                        self.result += response_body['speech']['text']

                elif response_body['code'] == 1002:
                    pass
                # 文本翻译
                elif response_body['code'] == 1003:
                    # 3.0
                    if 'tText' in response_body['translate']:
                        self.result += response_body['translate']['tText']
                        should_break = True
                    # 2.0
                    else:
                        self.result += response_body['translate']['text']
                # 任务完成
                elif response_body['code'] == 1001:
                    print("任务执行完成！")
                    should_break = True
                else:
                    print("执行出错：", response_body)
                    should_break = True
            else:
                # 语音合成
                if not isinstance(self.result, bytes):
                    self.result = b''
                self.result += response_body
        except Exception as e:
            self.result += response_body

        return should_break

    def recognize(self, audio, srcCode, dstCode):
        body = self._set_body("Recognize", srcCode, dstCode)
        # 建立连接
        response_body = self._create_connect(body)
        if response_body['code'] == 1000:
            # 读取wav文件
            frames = self._read_audio(audio)
            # 音频数据标志
            self._send_data(frames, self.type_audio)
            # 发送结束标志
            self._send_data(flag_end=True)
            result = self._receive_data

        print(f"识别结果：{result}")

        '''
        flag_trans = True
        if flag_trans:
            # 2.0版本的语音翻译（两步），必须注释self.re_connect
            print(f"翻译结果：{result}")
            result = self._receive_data
        '''
        return result

    def synthesize(self, text, srcCode, dstCode, save_path=''):
        body = self._set_body("Synthesize", srcCode, dstCode,
                              text=text, reqEngine="microsoft")
        response_body = self._create_connect(body)
        # 发送结束标志
        self._send_data(flag_end=True)
        if isinstance(response_body, dict) and response_body['code'] == 1000:
            print(response_body)
            frames = self._receive_data
        else:
            frames = response_body

        if len(frames) > 255:
            print(f"音频合成成功, 数据长度为 {len(frames)} 字节")
        else:
            print(f"音频合成失败, 数据长度为 {len(frames)} 字节")
            res = 255 / 0

        # 保存音频
        save_flag = False
        if save_flag:
            self._save_audio(save_path, frames)
        return

    def translate(self, text, srcCode, dstCode):
        # 文本翻译的代码逻辑
        body = self._set_body("Translate", srcCode, dstCode, text=text)
        result = self._create_connect(body)
        # 发送结束标志
        self._send_data(flag_end=True)
        print(f'翻译结果：{result}')
        return result

    def speech_translate(self, audio, srcCode, dstCode):
        body = self._set_body("SpeechTranslation", srcCode, dstCode)
        response_body = self._create_connect(body)
        if response_body['code'] == 1000:
            # 读取wav文件
            frames = self._read_audio(audio)
            # 音频数据标志
            self._send_data(frames, self.type_audio)
            # 发送结束标志
            self._send_data(flag_end=True)
            result = self._receive_data
            print("语音翻译结果：", result)

        return result

    def speech2text2speech(self, audio, srcCode, dstCode):
        text = self.recognize(audio, srcCode, dstCode)
        self.translate(text, srcCode, dstCode)
        print(f'两步语音翻译成功')


# class TestModle(TestTools):
#     def __init__(self, server_address):
#         super().__init__(server_address)
#         self.server_address = server_address
#         self.nums = 30  # 超时退出
#         signal.signal(signal.SIGALRM, self.timeout_handler)
#         signal.alarm(self.nums)

class TestModle(TestTools):
    def __init__(self, server_address):
        super().__init__(server_address)
        self.server_address = server_address
        self.nums = 30  # 超时退出
        signal.signal(signal.CTRL_C_EVENT, self.timeout_handler)
        os.kill(os.getpid(), signal.CTRL_C_EVENT)

    def timeout_handler(self, signum, frame):
        raise TimeoutException("Function timed out")

    @property
    def re_connect(self):

        def deal_connect():
            self.client_socket.close()
            self.client_socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(self.server_address)

        flag = True
        i = 1
        try:
            deal_connect()
        except TimeoutException:
            print("### 服务器拒绝连接，尝试重连 ###")
            while i < 5:
                print(f'第{i}次重连ing')
                try:
                    deal_connect()
                except TimeoutException:
                    flag = False
                else:
                    print('重连成功')
                    break
                finally:
                    i += 1
        finally:
            if not flag:
                print(f'第{i}次重连失败，程序退出')
                exit(1)

    def read_file(self, path):
        data = []
        with open(path, 'r') as f:
            for line in f:
                data.append(line.strip())
        return data

    # 支持语音识别 语音翻译

    def multi_connect(self, nums, srcCode, dstCode, type_num):
        func_name = "SpeechTranslation" if type_num == '3' else "Recognize"
        body = self._set_body(func_name, srcCode, dstCode)
        i = 1
        try:
            while i <= nums:
                response_body = self._create_connect(body)
                if response_body['code'] == 1000:
                    print(f"第{i}次 连接成功")
                    i += 1
        except TimeoutException:
            print(f"第{i}次 连接超时")
            signal.alarm(self.nums)  # 重置定时器

    def multi_connect_task(self, parameters):
        print("多次连接 再做任务")
        assert len(parameters) == 7
        func_model, func_name, nums, path, srcCode, dstCode, type_num = parameters
        self.multi_connect(nums, srcCode, dstCode, type_num)
        getattr(self, func_model)(func_name, path, srcCode, dstCode)

    # 文本翻译 合成

    def text2speech_task(self, func_name, path, srcCode, dstCode):
        texts = self.read_file(path)
        time1 = time.time()
        error_nums = 0
        sucess_times = 0
        i = 1
        for text in texts:
            text = json.loads(text)
            text = text['zh'] if srcCode == 'zh-CN' else text['en']
            try:
                time2 = time.time()
                print(f"输入文本：{text}")
                getattr(self, func_name)(text, srcCode, dstCode)
                time3 = time.time()
            except TimeoutException:
                print(f"第{i}条 响应超时")
                signal.alarm(self.nums)  # 重置定时器
                error_nums += 1
            except Exception as e:
                print(f"第{i}条 返回出错")
                error_nums += 1
            else:
                sucess_times += time3 - time2
                print(f"第{i}条耗时 {time3-time2} s")
            finally:
                i += 1

        self.client_socket.close()
        time4 = time.time()
        print(
            f"总共{len(texts)}条，测试出错{error_nums}条，成功数目耗时 {sucess_times} s, 总耗时 {time4-time1} s")

    # 识别 语音翻译 两步的语音翻译

    def speech2text_task(self, func_name, path, srcCode, dstCode):
        wav_files = self.read_file(path)
        time1 = time.time()
        error_nums = 0
        sucess_times = 0
        i = 1
        for audio in wav_files:
            try:
                time2 = time.time()
                getattr(self, func_name)(audio, srcCode, dstCode)
                time3 = time.time()
            except TimeoutException:
                print(f"第{i}条 响应超时")
                signal.alarm(self.nums)  # 重置定时器
                error_nums += 1
            except Exception as e:
                print(f"第{i}条 数据返回出错")
                error_nums += 1
            else:
                sucess_times += time3 - time2
                print(f"第{i}条耗时 {time3-time2} s")
            finally:
                self.re_connect
                i += 1

        self.client_socket.close()
        time4 = time.time()
        print(
            f"总共{len(wav_files)}条，测试出错{error_nums}条，成功数目耗时 {sucess_times} s, 总耗时 {time4-time1} s")


def multi_processing(parameters, max_workers=16, thread=True):
    print("多线程/进程任务")
    assert len(parameters) == 6
    server_address, func_model, func_name, path, srcCode, dstCode = parameters
    # 实例化
    instances = [TestModle(server_address) for _ in range(max_workers)]
    process_func = concurrent.futures.ThreadPoolExecutor if thread else concurrent.futures.ProcessPoolExecutor
    with process_func(max_workers=max_workers) as executor:
        # 提交多个任务给线程/进程池
        tasks = [executor.submit(
            getattr(ins, func_model), func_name, path, srcCode, dstCode) for ins in instances]
        # # 获取任务的结果
        # for future in concurrent.futures.as_completed(tasks):
        #     try:
        #         result = future.result()
        #         print(result)
        #         # 处理任务的返回结果
        #     except Exception as e:
        #         pass


def async_processing(parameters, max_workers=4):
    print("协程任务")
    assert len(parameters) == 6
    server_address, func_model, func_name, path, srcCode, dstCode = parameters
    # 实例化
    instances = [TestModle(server_address) for _ in range(max_workers)]

    async def deal_func():
        # 创建任务
        tasks = [getattr(ins, func_model)(func_name, path, srcCode, dstCode)
                 for ins in instances]

        # 开始执行任务
        results = await asyncio.gather(*tasks)
        print(results)

    # 执行主协程
    asyncio.run(deal_func())


def parse_args():
    parser = argparse.ArgumentParser(description='测试参数设置')
    parser.add_argument('--model', type=str,
                        default='speech2text', help='speech2text text2speech multi_connect multi_processing async_processing')
    parser.add_argument('--type', type=str, default='2',
                        help='O 文本翻译 1 语音合成 2 语音识别 3 语音翻译 4 识别再翻译')
    parser.add_argument('--file_path', type=str, help='文本或音频列表路径')
    parser.add_argument('--src_code', type=str, default='zh-CN', help='源语言代码')
    parser.add_argument('--dst_code', type=str, default='en-US', help='目标语言代码')
    parser.add_argument('--max_nums', type=int, default=200, help='最大连接数')

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    srcCode = args.src_code
    dstCode = args.dst_code
    server_address = ('35.74.61.68', 5050)  # 3.0测试环境
    # server_address = ('35.74.61.68', 7889)  # 2.0测试环境
    mytest = TestModle(server_address)
    func_dict = {'0': 'translate', '1': 'synthesize',
                 '2': 'recognize', '3': 'speech_translate',
                 '4': 'speech2text2speech'}

    if '2' <= args.type <= '4':
        func_task = 'speech2text_task'
    else:
        func_task = 'text2speech_task'

    if args.model == 'speech2text' and args.type > '1':
        getattr(mytest, func_task)(
            func_dict[args.type], args.file_path, srcCode, dstCode)
    elif args.model == 'text2speech' and '0' <= args.type < '2':
        getattr(mytest, func_task)(
            func_dict[args.type], args.file_path, srcCode, dstCode)
    elif args.model == 'multi_connect':
        getattr(mytest, 'multi_connect')(
            args.max_nums, srcCode, dstCode, args.type)
    elif args.model == 'multi_connect_task':
        getattr(mytest, 'multi_connect_task')(
            (func_task, func_dict[args.type], args.max_nums, args.file_path, srcCode, dstCode, args.type),)
    elif args.model == 'multi_processing':
        multi_processing((server_address, func_task,
                         func_dict[args.type], args.file_path, srcCode, dstCode),)
    elif args.model == 'async_processing':
        async_processing((server_address, func_task,
                         func_dict[args.type], args.file_path, srcCode, dstCode),)
    else:
        print(f'输入参数有误：{args}')


if __name__ == "__main__":
    main()

from aiogram import Bot, Dispatcher, executor, types
import os
import logging
import fnmatch

API_TOKEN = "YOUR API"
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands="start")
async def start_msg(message: types.Message):
    mchat = str(message.chat.id)
    mdir = ".\\" + mchat + "\\"
    if os.path.isdir(mdir):
        pass
    else:
        os.mkdir(mdir)
    await message.answer(f"Done! You're individual folder key is: '{mchat}'")
@dp.message_handler(commands="sendfile")
async def send_file1(message: types.Message):
    await message.answer('Send file')
    @dp.message_handler(content_types=['document'])
    async def send_file(message: types.Message):
        try:
            mchat = str(message.chat.id)
            mdir = ".\\" + mchat + "\\"
            file_name = message.document.file_name
            savedir = mdir + file_name
            print(savedir)
            file_info = await bot.get_file(message.document.file_id)
            downloaded_file = await bot.download_file(file_info.file_path)
            with open(savedir, 'wb') as new_file:
                new_file.write(downloaded_file.getvalue())
        except Exception as e:
            print(e)
            message.answer(f'ERROR! {e}')

@dp.message_handler(commands="findfiles")
async def list_files_by_id(message: types.Message):
    mchat = str(message.chat.id)
    arguments = message.get_args()
    print(arguments)
    lst = []
    for file in os.listdir(f".\\{mchat}\\"):
        if fnmatch.fnmatch(file, '*'):
            lst.append(file)
    joined_lst = "\n".join(lst)
    await message.answer(f'Founded some files! \n{joined_lst}')
@dp.message_handler(commands="getfiles")
async def get_file(message: types.Message):
    arguments = message.get_args()
    print(arguments)
    argsget = arguments.split(' ')
    print(argsget)
    f = open(f".\\{argsget[0]}\\{argsget[1]}", "rb")
    await message.answer_document(f)
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
